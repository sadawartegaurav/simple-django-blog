# Generated by Django 2.2.5 on 2019-09-27 04:39

from django.db import migrations, models
import django.db.models.deletion
import django.views.generic.list


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190924_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResultsView',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Post')),
            ],
            bases=(django.views.generic.list.ListView, 'blog.post'),
        ),
    ]
