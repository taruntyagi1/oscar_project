# Generated by Django 3.2.16 on 2023-01-02 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0042_auto_20221229_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(through='catalogue.ProductCategory', to='catalogue.category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='recommended_products',
            field=models.ManyToManyField(blank=True, help_text='These are products that are recommended to accompany the main product.', through='catalogue.ProductRecommendation', to='catalogue.product', verbose_name='Recommended products'),
        ),
    ]
