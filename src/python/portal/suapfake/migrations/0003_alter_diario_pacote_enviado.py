# Generated by Django 4.0.4 on 2022-06-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("suapfake", "0002_alter_diario_options_remove_diario_codigo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diario",
            name="pacote_enviado",
            field=models.JSONField(
                default={
                    "alunos": [
                        {
                            "email": "nome.compelto@academico.ifrn.edu.br",
                            "email_secundario": "nome.completo@hotmail.com",
                            "id": 1,
                            "matricula": "20183000010001",
                            "nome": "Nome completo do aluno",
                            "polo": None,
                            "situacao": "ativo",
                        }
                    ],
                    "campus": {
                        "descricao": "NOME COMPLETO DO CAMPUS",
                        "id": 1,
                        "sigla": "NCC",
                    },
                    "componente": {
                        "descricao": "Bancos de Dados",
                        "descricao_historico": "Bancos de Dados",
                        "id": 1,
                        "optativo": False,
                        "periodo": None,
                        "qtd_avaliacoes": 2,
                        "sigla": "TEC.0001",
                        "tipo": 1,
                    },
                    "curso": {
                        "codigo": "00001",
                        "descricao": "Tecnologia em Redes de Computadores - Nome Completo do Campus",
                        "id": 1,
                        "nome": "Tecnologia em Redes de Computadores",
                    },
                    "diario": {
                        "descricao": "Bancos de Dados",
                        "descricao_historico": "Bancos de Dados",
                        "id": 1,
                        "sigla": "TEC.0001",
                        "situacao": "Aberto",
                    },
                    "polo": None,
                    "professores": [
                        {
                            "email": "nome.sobrenome@ifrn.edu.br",
                            "email_secundario": "nome.sobrenome@gmail.com",
                            "id": 1,
                            "login": "1234567",
                            "nome": "Nome completo de um professor principal",
                            "status": "ativo",
                            "tipo": "Principal",
                        }
                    ],
                    "turma": {"codigo": "20221.6.00001.1E", "id": 1},
                },
                verbose_name="pacote a enviar/enviado",
            ),
        ),
    ]
