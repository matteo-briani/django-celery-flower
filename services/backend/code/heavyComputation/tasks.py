from celery import shared_task
from celery_once import QueueOnce
from .models import HeavyComputation

@shared_task(base=QueueOnce, bind=True)
def heavy_computation_task(self, heavy_computation_uuid = None):
    if not heavy_computation_uuid:
        raise Exception
    hc = HeavyComputation.objects.get(uuid = heavy_computation_uuid)
    hc.task_uuid = self.request.id
    hc.save()
    result = hc.compute()
    hc.task_uuid = None
    hc.save()
    return result
