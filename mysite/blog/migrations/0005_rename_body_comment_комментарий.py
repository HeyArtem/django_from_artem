# Generated by Django 4.2.1 on 2023-05-16 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_name_comment_имя'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='Комментарий',
        ),
    ]
