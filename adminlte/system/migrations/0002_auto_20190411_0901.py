# Generated by Django 2.1.5 on 2019-04-11 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuinfo',
            options={'ordering': ['priority'], 'verbose_name': '菜单', 'verbose_name_plural': '菜单'},
        ),
        migrations.RemoveField(
            model_name='menuinfo',
            name='order_by',
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='icons/user2-160x160.jpg', null=True, upload_to='icons/%Y/%m/%d', verbose_name='照片'),
        ),
    ]
