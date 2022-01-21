from django.core.management.base import BaseCommand
from heavyComputation.tasks import heavy_computation_task
from celery_once import AlreadyQueued

class Command(BaseCommand):
    help = 'Submit heavy computation task'

    def handle(self, *args, **options):

        try:
            heavy_computation_task.delay()
        except AlreadyQueued:
            print('Task already queued, submission is locked')
