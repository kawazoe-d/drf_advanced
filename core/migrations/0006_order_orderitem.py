# Generated by Django 3.1.7 on 2022-11-19 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transacrion_id', models.TextField(null=True)),
                ('code', models.TextField()),
                ('ambassador_email', models.TextField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.TextField()),
                ('address', models.TextField(null=True)),
                ('city', models.TextField(null=True)),
                ('country', models.TextField(null=True)),
                ('zip', models.TextField(null=True)),
                ('complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('admin_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ambassador_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='core.order')),
            ],
        ),
    ]
