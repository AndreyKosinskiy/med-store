# Generated by Django 2.2.6 on 2019-10-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_store', '0005_auto_20191016_1214'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Good',
            new_name='ProductItem',
        ),
        migrations.AddField(
            model_name='lot',
            name='product_item_batch',
            field=models.CharField(default=0, max_length=120),
            preserve_default=False,
        ),
    ]
