from django.core.management.base import BaseCommand
from django.conf import settings
from recipe.models import Ingredient
import os
import json


class Command(BaseCommand):
    help = 'Add data to db'

    def handle(self, *args, **options):
        file_name = os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')
        with open (file_name) as f:
            data = json.load(f)

        for i in data:
            name = i['name']
            measurement_unit = i['measurement_unit']
            Ingredient.objects.create(name=name,measurement_unit=measurement_unit)
