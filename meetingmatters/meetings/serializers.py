import json
from rest_framework import serializers
from . import models

class MeetingSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Meeting
        queryset = model.objects.all().prefetch_related('tags').select_related('venue')
        exclude = ['region', 'speakers', 'attendees', 'venue_name', 'venue_additional']

    def topics(self, meeting):
        return [tag.name for tag in meeting.tags.all()]

    def venue(self, meeting):
        venue = meeting.venue
        return {
            'name': venue.name,
            'address': venue.address,
            'location': venue.location.json,
            'notes': meeting.venue_additional
        }
