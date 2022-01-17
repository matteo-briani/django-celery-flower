from django.contrib import admin
from .models import HeavyComputation

@admin.register(HeavyComputation)
class HeavyComputationAdmin(admin.ModelAdmin):
    pass

