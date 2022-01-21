from celery import shared_task
from celery_once import QueueOnce
from .models import HeavyComputation

@shared_task(base=QueueOnce, bind=True)
def heavy_computation_task(self, task_number = 0):
   hc = HeavyComputation.objects.all()[task_number]
   hc.compute()
