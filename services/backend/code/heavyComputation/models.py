from django.db import models
import uuid
from time import sleep
from random import randint
from enum import Enum

class CustomComputationException(Exception):
    pass

class HeavyComputation(models.Model):

    STATES = (
        ('Initialized', 'Initialized'),
        ('Scheduled', 'Scheduled'),
        ('Computing', 'Computing'),
        ('Computed', 'Computed'),
        ('Frozen', 'Frozen'),
        ('Error', 'Error'),
    )

    uuid         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name         = models.CharField('Name', max_length=36)
    status       = models.CharField('Status', max_length=36, choices=STATES, default='Initialized', blank=True, null=False)

    def __str__(self):
        return f'HeavyCompuation - name "{self.name}" - status "{self.status}"'

    def save(self, *args, **kwargs):
        allowed_states_choices = [status[0] for status in self.STATES]
        if self.status not in allowed_states_choices:
            raise Exception('Sorry, the report status "{}" is not valid. Allowed states are: "{}"'.format(self.status, allowed_states_choices))
        super(HeavyComputation, self).save(*args, **kwargs)  

    def compute(self):

        sleep(30) 
        # Simulate unrecoverable error
        if randint(1, 10) <= 3:
            raise CustomComputationException('A -mocked- unrecovarable error occured during computation')
        sleep(30) 
        # Simulate a recovarable error during computation
        if randint(1, 10) <= 5:
            return 'report computed but encountered computational errors'
        return 'report computed successfully' 

