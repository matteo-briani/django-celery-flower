from celery import shared_task
from celery_once import QueueOnce
from .models import HeavyComputation

@shared_task(base=QueueOnce, bind=True)
def heavy_computation_task(self):
   hc = HeavyComputation.objects.all()[0]
   hc.compute()
