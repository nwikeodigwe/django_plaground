# Generated by Django 5.0.7 on 2024-08-01 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
