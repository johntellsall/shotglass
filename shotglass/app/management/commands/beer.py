
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('beer')
        print(f'{args=}') 
        print(f'{options=}')