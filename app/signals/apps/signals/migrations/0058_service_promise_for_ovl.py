# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2021 Gemeente Amsterdam
# Generated by Django 2.1.7 on 2019-05-27 14:54

from django.db import migrations

CHANGE = {
    'wegen-verkeer-straatmeubilair': {
        'lantaarnpaal-straatverlichting': {
            'handling': 'LIGHTING',
        },
    },
}


def change_categories(apps, schema_editor):
    Category = apps.get_model('signals', 'Category')
    for main_slug, data in CHANGE.items():
        if not data:
            continue

        main_category = Category.objects.get(slug=main_slug, parent__isnull=True)
        for sub_slug, sub_data in data.items():
            sub_category = Category.objects.get(slug=sub_slug, parent=main_category)

            # mutate here
            if 'handling' in sub_data:
                sub_category.handling = sub_data['handling']

            sub_category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0057_new_handling_message'),
    ]

    operations = [
        migrations.RunPython(change_categories),
    ]