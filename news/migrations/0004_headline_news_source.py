# Generated by Django 5.0.4 on 2024-04-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_delete_intrest_remove_headline_news_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='news_source',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
