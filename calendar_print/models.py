from django.db import models
from django.utils import timezone

class Event(models.Model):
    planning_center_instance_id = models.IntegerField(
        primary_key=True,
        unique=True,
    )
    planning_center_event_id = models.IntegerField()
    just_imported = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def readable_times(self):
        return {
            'date': timezone.localtime(self.start_time).strftime('%A, %B %-d'),
            'start_time': timezone.localtime(self.start_time).strftime('%-I:%M %p'),
            'end_time': timezone.localtime(self.end_time).strftime('%-I:%M %p'),
        }

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('start_time',)