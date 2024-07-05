# Generated by Django 5.0.6 on 2024-07-01 03:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CardInfo", "0003_rename_skill_damnage_pokemoncardskill_skill_damage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemoncardskill",
            name="skill_cost",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="能量"
            ),
        ),
        migrations.AlterField(
            model_name="pokemoncardskill",
            name="skill_damage",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="傷害"
            ),
        ),
        migrations.AlterField(
            model_name="pokemoncardskill",
            name="skill_effect",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="特效"
            ),
        ),
        migrations.AlterField(
            model_name="pokemoncardskill",
            name="skill_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="名稱"
            ),
        ),
        migrations.AlterField(
            model_name="pokemoncardskill",
            name="skill_type",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="種類"
            ),
        ),
    ]
