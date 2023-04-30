# Generated by Django 4.1.7 on 2023-04-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0007_ambiente_cor_sutil_historicalambiente_cor_sutil"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ambiente",
            name="cor",
        ),
        migrations.RemoveField(
            model_name="ambiente",
            name="cor_sutil",
        ),
        migrations.RemoveField(
            model_name="historicalambiente",
            name="cor",
        ),
        migrations.RemoveField(
            model_name="historicalambiente",
            name="cor_sutil",
        ),
        migrations.AddField(
            model_name="ambiente",
            name="cor_degrade",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #53296d; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#53296d</span> <span style='background: #396ba7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#396ba7</span> <span style='background: #315810; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#315810</span> <span style='background: #ae8133; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ae8133</span> <span style='background: #d05623; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#d05623</span> <span style='background: #f54f3b; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#f54f3b</span>",
                max_length=255,
                verbose_name="cor degradê do ambiente",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ambiente",
            name="cor_mestra",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #a04ed0; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#a04ed0</span> <span style='background: #396ba7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#396ba7</span> <span style='background: #559c1a; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#559c1a</span> <span style='background: #fabd57; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#fabd57</span> <span style='background: #fd7941; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#fd7941</span> <span style='background: #f54f3b; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#f54f3b</span>",
                max_length=255,
                verbose_name="cor mestra do ambiente",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ambiente",
            name="cor_progresso",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #ecdafa; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ecdafa</span> <span style='background: #b4d0f2; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#b4d0f2</span> <span style='background: #d2f4b7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#d2f4b7</span> <span style='background: #ffebca; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffebca</span> <span style='background: #ffd1be; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffd1be</span> <span style='background: #ffbab2; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffbab2</span>",
                max_length=255,
                verbose_name="cor do progresso do ambiente",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalambiente",
            name="cor_degrade",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #53296d; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#53296d</span> <span style='background: #396ba7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#396ba7</span> <span style='background: #315810; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#315810</span> <span style='background: #ae8133; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ae8133</span> <span style='background: #d05623; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#d05623</span> <span style='background: #f54f3b; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#f54f3b</span>",
                max_length=255,
                verbose_name="cor degradê do ambiente",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalambiente",
            name="cor_mestra",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #a04ed0; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#a04ed0</span> <span style='background: #396ba7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#396ba7</span> <span style='background: #559c1a; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#559c1a</span> <span style='background: #fabd57; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#fabd57</span> <span style='background: #fd7941; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#fd7941</span> <span style='background: #f54f3b; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#f54f3b</span>",
                max_length=255,
                verbose_name="cor mestra do ambiente",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalambiente",
            name="cor_progresso",
            field=models.CharField(
                default="#a04ed0",
                help_text="Escolha uma cor em RGB. Ex.: <span style='background: #ecdafa; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ecdafa</span> <span style='background: #b4d0f2; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#b4d0f2</span> <span style='background: #d2f4b7; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#d2f4b7</span> <span style='background: #ffebca; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffebca</span> <span style='background: #ffd1be; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffd1be</span> <span style='background: #ffbab2; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#ffbab2</span>",
                max_length=255,
                verbose_name="cor do progresso do ambiente",
            ),
            preserve_default=False,
        ),
    ]
