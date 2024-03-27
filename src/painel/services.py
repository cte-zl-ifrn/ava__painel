import logging
import concurrent
import re
import json
import urllib.parse
import sentry_sdk
from typing import Dict, List, Union, Any
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
import requests
from http.client import HTTPException
from .models import Ambiente, Curso


CODIGO_DIARIO_REGEX = re.compile("^(\d\d\d\d\d)\.(\d*)\.(\d*)\.(.*)\.(\w*\.\d*)(#\d*)?$")
CODIGO_DIARIO_ANTIGO_ELEMENTS_COUNT = 5
CODIGO_DIARIO_NOVO_ELEMENTS_COUNT = 6
CODIGO_DIARIO_SEMESTRE_INDEX = 0
CODIGO_DIARIO_PERIODO_INDEX = 1
CODIGO_DIARIO_CURSO_INDEX = 2
CODIGO_DIARIO_TURMA_INDEX = 3
CODIGO_DIARIO_DISCIPLINA_INDEX = 4
CODIGO_DIARIO_ID_DIARIO_INDEX = 5

CODIGO_COORDENACAO_REGEX = re.compile("^(\w*)\.(\d*)(.*)*$")
CODIGO_COORDENACAO_ELEMENTS_COUNT = 3
CODIGO_COORDENACAO_CAMPUS_INDEX = 0
CODIGO_COORDENACAO_CURSO_INDEX = 1
CODIGO_COORDENACAO_SUFIXO_INDEX = 2

CODIGO_PRATICA_REGEX = re.compile("^(\d\d\d\d\d)\.(\d*)\.(\d*)\.(.*)\.(\d{11,14}\d*)$")
CODIGO_PRATICA_ELEMENTS_COUNT = 5
CODIGO_PRATICA_SUFIXO_INDEX = 4

CURSOS_CACHE = {}

CHANGE_URL = re.compile("/course/view.php\?")


def requests_get(url, headers={}, encoding="utf-8", decode=True, **kwargs):
    response = requests.get(url, headers=headers, **kwargs)

    if response.ok:
        byte_array_content = response.content
        return byte_array_content.decode(encoding) if decode and encoding is not None else byte_array_content
    else:
        exc = HTTPException("%s - %s" % (response.status_code, response.reason))
        exc.status = response.status_code
        exc.reason = response.reason
        exc.headers = response.headers
        exc.url = url
        raise exc


def get_json(url, headers={}, encoding="utf-8", json_kwargs=None, **kwargs):
    content = requests_get(url, headers=headers, encoding=encoding, **kwargs)
    return json.loads(content, **(json_kwargs or {}))


def get_json_api(ava: Ambiente, service: str, **params: dict):
    try:
        if params is not None:
            querystring = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        else:
            querystring = ""
        url = f"{ava.base_api_url}/?{service}&{querystring}"
        content = get_json(url, headers={"Authentication": f"Token {ava.token}"})
        return content
    except Exception as e:
        logging.error(e)
        sentry_sdk.capture_exception(e)


def get_diarios(
    username: str,
    semestre: str = None,
    situacao: str = None,
    disciplina: str = None,
    curso: str = None,
    ambiente: str = None,
    q: str = None,
    page: int = 1,
    page_size: int = 21,
) -> dict:
    def _get_diarios(params: Dict[str, Any]):
        def _merge_course(diario: dict, ambiente: dict):
            def _merge_curso(diario: dict, diario_re: re.Match):
                if not diario_re and len(diario_re[0]) not in (
                    CODIGO_DIARIO_ANTIGO_ELEMENTS_COUNT,
                    CODIGO_DIARIO_NOVO_ELEMENTS_COUNT,
                    CODIGO_COORDENACAO_ELEMENTS_COUNT,
                    CODIGO_PRATICA_ELEMENTS_COUNT,
                ):
                    return

                if len(diario_re[0]) == CODIGO_COORDENACAO_ELEMENTS_COUNT:
                    co_curso = diario_re[0][CODIGO_COORDENACAO_CURSO_INDEX]
                else:
                    co_curso = diario_re[0][CODIGO_DIARIO_CURSO_INDEX]

                if co_curso not in CURSOS_CACHE and CURSOS_CACHE.get(co_curso, None) is None:
                    curso = Curso.objects.filter(codigo=co_curso).first()
                    if curso:
                        CURSOS_CACHE[co_curso] = curso

                curso = CURSOS_CACHE.get(co_curso, Curso(codigo=co_curso, nome=f"Curso: {co_curso}"))
                diario["curso"] = {"codigo": curso.codigo, "nome": curso.nome}

            def _merge_turma(diario: dict, diario_re: re.Match):
                if len(diario_re) > 0 and len(diario_re[0]) >= CODIGO_DIARIO_TURMA_INDEX:
                    diario["turma"] = ".".join(diario_re[0][0 : CODIGO_DIARIO_TURMA_INDEX + 1])

            def _merge_componente(diario: dict, diario_re: re.Match):
                if len(diario_re) > 0 and len(diario_re[0]) >= CODIGO_DIARIO_DISCIPLINA_INDEX:
                    diario["componente"] = diario_re[0][CODIGO_DIARIO_DISCIPLINA_INDEX]

            def _merge_id_diario(diario: dict, diario_re: re.Match):
                if len(diario_re) > 0 and len(diario_re[0]) >= CODIGO_DIARIO_ID_DIARIO_INDEX:
                    id_diario_hash = diario_re[0][CODIGO_DIARIO_ID_DIARIO_INDEX]
                    diario["id_diario"] = id_diario_hash
                    diario["id_diario_clean"] = int(id_diario_hash[1:]) if id_diario_hash else None

            def _merge_extra_urls(diario: dict, ava: Ambiente):
                id_diario = diario.get("id_diario_clean", None)

                if diario.get("can_set_visibility") and id_diario:
                    diario["can_check_grades"] = True
                    diario["checkgradesurl"] = reverse(
                        "painel:checkgrades", kwargs={"id_ambiente": ava["ambiente"]["id"], "id_diario": id_diario}
                    )
                    # diario["can_view_syncsurl"] = True
                    # diario["syncsurl"] = reverse("painel:syncs", kwargs={"id_diario": id_diario})

                    diario["mensagemurl"] = f"{settings.OAUTH["BASE_URL"]}/edu/enviar_mensagem/?diario={id_diario}"

                print("id_diario:", id_diario)
                if id_diario:
                    diario["suapsurl"] = f"{settings.OAUTH["BASE_URL"]}/edu/meu_diario/{id_diario}/1/"
                    if diario.get("can_set_visibility"):
                        diario["gradesurl"] = re.sub("/course/view", "/grade/report/grader/index", diario["viewurl"])
                    else:
                        diario["gradesurl"] = re.sub("/course/view", "/grade/report/overview/index", diario["viewurl"])

                    # try:
                    #     # TODO: Melhor a performance aqui
                    #     ultima = Solicitacao.objects.ultima_do_diario(id_diario)

                    #     if ultima is not None:
                    #         diario["syncsurl"] = reverse("painel:syncs", kwargs={"id_diario": id_diario})
                    #         print("ultima:", ultima.respondido)
                    #         diario["coordenacaourl"] = ultima.respondido.get("url_sala_coordenacao")
                    # except Exception as e:
                    #     logging.error(e)
                    #     sentry_sdk.capture_exception(e)

            def _merge_aluno(diario: dict, diario_re: re.Match):
                if diario_re and len(diario_re[0]) > CODIGO_PRATICA_SUFIXO_INDEX:
                    diario["componente"] = diario_re[0][CODIGO_PRATICA_SUFIXO_INDEX]

            codigo = diario["shortname"]
            diario_re = CODIGO_DIARIO_REGEX.findall(codigo)
            coordenacao_re = CODIGO_COORDENACAO_REGEX.findall(codigo)
            pratica_re = CODIGO_PRATICA_REGEX.findall(codigo)

            if diario_re:
                _merge_curso(diario, diario_re)
                _merge_turma(diario, diario_re)
                _merge_componente(diario, diario_re)
                _merge_id_diario(diario, diario_re)
                _merge_extra_urls(diario, ambiente)
            elif pratica_re:
                _merge_curso(diario, pratica_re)
                _merge_turma(diario, pratica_re)
                _merge_aluno(diario, pratica_re)
            elif coordenacao_re:
                _merge_curso(diario, coordenacao_re)
            return {**diario, **ambiente}

        try:
            ambiente = params["ambiente"]
            ambientedict = {
                "ambiente": {
                    "id": ambiente.id,
                    "titulo": ambiente.nome,
                    "cor_mestra": ambiente.cor_mestra,
                }
            }

            querystrings = {k: v for k, v in params.items() if k not in ["ambiente", "results"]}

            if "q" in querystrings:
                querystrings["q"] = urllib.parse.quote(querystrings["q"])

            result = get_json_api(ambiente, "get_diarios", **querystrings)

            for k, v in params["results"].items():
                if k in result:
                    if k in ["diarios", "coordenacoes", "praticas"]:
                        params["results"][k] += [_merge_course(diario, ambientedict) for diario in result[k] or []]
                    else:
                        params["results"][k] += result[k] or []

        except Exception as e:
            logging.error(e)
            sentry_sdk.capture_exception(e)

    def deduplicate_and_sort(list_of_dict: Union[None, List[Dict[str, str]]], reverse: bool = False):
        deduplicated = [{"id": x, "label": y} for x, y in ({x["id"]: x["label"] for x in list_of_dict}).items()]
        sortedlist = sorted(deduplicated, key=lambda e: e["label"], reverse=reverse)
        return sortedlist

    results = {
        "semestres": [],
        "ambientes": Ambiente.as_dict(),
        "disciplinas": [],
        "cursos": [],
        "diarios": [],
        "coordenacoes": [],
        "praticas": [],
    }

    has_ambiente = ambiente != "" and ambiente is not None and f"{ambiente}".isnumeric()

    ambientes = [
        ava
        for ava in Ambiente.objects.filter(active=True)
        if (has_ambiente and int(ambiente) == ava.id) or not has_ambiente
    ]

    requests = [
        {
            "ambiente": ava,
            "username": username,
            "semestre": semestre,
            "situacao": situacao,
            "disciplina": disciplina,
            "curso": curso,
            "q": q,
            "page": page,
            "page_size": page_size,
            "results": results,
        }
        for ava in ambientes
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(_get_diarios, requests)

    results["semestres"] = [{"id": "", "label": "Semestres... "}] + deduplicate_and_sort(
        results["semestres"], reverse=True
    )
    results["disciplinas"] = [{"id": "", "label": "Disciplinas..."}] + deduplicate_and_sort(results["disciplinas"])
    results["ambientes"] = [
        {
            "label": "Ambientes...",
            "id": "",
            "color": None,
        }
    ] + sorted(results["ambientes"], key=lambda e: e["label"])

    results["coordenacoes"] = sorted(results["coordenacoes"], key=lambda e: e["fullname"])
    results["praticas"] = sorted(results["praticas"], key=lambda e: e["fullname"])
    cursos = {c.codigo: c.nome for c in Curso.objects.filter(codigo__in=[x["id"] for x in results["cursos"]])}
    for c in results["cursos"]:
        if c["id"] in cursos:
            c["label"] = f"{cursos[c['id']]}"
        else:
            c["label"] = f"Curso [{c['id']}], favor solicitar o cadastro"
    results["cursos"] = [{"id": "", "label": "Cursos..."}] + deduplicate_and_sort(results["cursos"])

    return results


def get_atualizacoes_counts(username: str) -> dict:
    def _callback(params):
        try:
            ava = params["ava"]

            counts = get_json_api(ava, "get_atualizacoes_counts", username=params["username"])

        except Exception as e:
            logging.error(e)
            sentry_sdk.capture_exception(e)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = {
            "atualizacoes": [],
            "unread_notification_total": 0,
            "unread_conversations_total": 0,
        }
        requests = [
            {
                "username": username,
                "ava": ava,
                "results": results,
            }
            for ava in Ambiente.objects.filter(active=True)
        ]
        executor.map(_callback, requests)

    results["atualizacoes"] = sorted(results["atualizacoes"], key=lambda e: e["ambiente"]["titulo"])
    return results


def set_favourite_course(username: str, ava: str, courseid: int, favourite: int) -> dict:
    ava = get_object_or_404(Ambiente, nome=ava)
    return get_json_api(ava, "set_favourite_course", username=username, courseid=courseid, favourite=favourite)


def set_visible_course(username: str, ava: str, courseid: int, visible: int) -> dict:
    ava = get_object_or_404(Ambiente, nome=ava)
    return get_json_api(ava, "set_visible_course", username=username, courseid=courseid, visible=visible)
