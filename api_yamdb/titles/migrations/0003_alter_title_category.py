# Generated by Django 3.2 on 2023-09-06 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_auto_20230906_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.category', verbose_name='Категория'),
        ),
    ]
