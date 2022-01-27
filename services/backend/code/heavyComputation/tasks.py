from celery import shared_task
from celery_once import QueueOnce
from .models import HeavyComputation

@shared_task(base=QueueOnce, bind=True)
def heavy_computation_task(self, heavy_computation_uuid = None):
    if not heavy_computation_uuid:
        raise Exception
    hc = HeavyComputation.objects.get(uuid = heavy_computation_uuid)
    result = hc.compute()
    if result == 'report computed but encountered computational errors':
        hc.status = 'Error'
    if result == 'report computed successfully':
        hc.status = 'Computed'
    hc.save()
    return result
