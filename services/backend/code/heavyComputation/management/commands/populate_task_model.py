from django.core.management.base import BaseCommand
from heavyComputation.models import HeavyComputation

class Command(BaseCommand):
    help = 'Populate HeavyComputation task'

    def handle(self, *args, **options):

        for i in range(10):
            HeavyComputation.objects.create(name=f'heavy_computation_{i}')
