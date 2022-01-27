from celery import shared_task
from celery_once import QueueOnce
from .models import HeavyComputation

@shared_task(base=QueueOnce, bind=True)
def heavy_computation_task(self, heavy_computation_uuid = None):
    if not heavy_computation_uuid:
        raise Exception
    hc = HeavyComputation.objects.get(uuid = heavy_computation_uuid)
    result = hc.compute()
    return result
