from django.core.management.base import BaseCommand
from heavyComputation.tasks import heavy_computation_task
from heavyComputation.models import HeavyComputation
from celery_once import AlreadyQueued

class Command(BaseCommand):
    help = 'Submit heavy computation task'

    def add_arguments(self, parser):
        parser.add_argument(
            '--task_number',
            type=int,
            default=0,
            help='specifies the task number',
            )

    def handle(self, *args, **options):
        # Parse task number
        task_number = options['task_number']

        try:
            # translate task to uuid
            hc = HeavyComputation.objects.all().order_by('name')[task_number]
            heavy_computation_task.delay(heavy_computation_uuid = hc.uuid)
        except AlreadyQueued:
            print('Task already queued, submission is locked')
        except Exception:
            raise

