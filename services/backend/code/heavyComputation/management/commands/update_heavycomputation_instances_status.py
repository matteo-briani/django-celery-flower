from django.core.management.base import BaseCommand
from heavyComputation.models import HeavyComputation
from django.db import transaction
import requests

FLOWER_ORIGIN = 'http://flower-dcf:8888'

class Command(BaseCommand):
    help = 'Update HeavyComputation models status'

    def handle(self, *args, **options):

        s = requests.Session()

        # From Flower to Django
        with transaction.atomic():

            # -- Set task in the STARTED state
            # From Flower to Django
            r = s.get(f'{FLOWER_ORIGIN}/api/tasks?offset=0&state=STARTED')
            data = r.json()
            for key, value in data.items():
                kwargs = value['kwargs']
                begin_uuid_idx = kwargs.find('UUID')
                hc_uuid = kwargs[begin_uuid_idx+6:begin_uuid_idx+42]
                hc = HeavyComputation.objects.get(uuid = hc_uuid)
                hc.status = 'Computing'
                hc.save()

            # From Django to Flower
            for hc in HeavyComputation.objects.all():
                if hc.status == "Computing":
                    is_still_computing = False
                    # Check if task has failed, is it still computing?
                    for _, value in data.items():
                        if str(hc.uuid) in value['kwargs']:
                            is_still_computing = True
                    if not is_still_computing:
                        hc.status = 'Error'
                        hc.save()


            # -- Set task in the RECEIVED state
            # From Flower to Django
            r = s.get(f'{FLOWER_ORIGIN}/api/tasks?offset=0&state=RECEIVED')
            data = r.json()
            for key, value in data.items():
                kwargs = value['kwargs']
                begin_uuid_idx = kwargs.find('UUID')
                hc_uuid = kwargs[begin_uuid_idx+6:begin_uuid_idx+42]
                hc = HeavyComputation.objects.get(uuid = hc_uuid)
                hc.status = 'Scheduled'
                hc.save()

            # From Django to Flower
            for hc in HeavyComputation.objects.all():
                if hc.status == "Scheduled":
                    is_still_computing = False
                    # Check if task has failed, is it still computing?
                    for _, value in data.items():
                        if str(hc.uuid) in value['kwargs']:
                            is_still_computing = True
                    if not is_still_computing:
                        hc.status = 'Error'
                        hc.save()
