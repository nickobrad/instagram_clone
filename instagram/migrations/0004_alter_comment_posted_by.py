# Generated by Django 3.2.7 on 2021-09-13 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_auto_20210913_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instagram.profile'),
        ),
    ]