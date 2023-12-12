# Generated by Django 4.2.7 on 2023-12-10 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awork_desktop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipadress', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('query_id', models.TextField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_books', to='awork_desktop.userdesk')),
            ],
        ),
    ]