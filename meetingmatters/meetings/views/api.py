from rest_framework.generics import ListAPIView
from .. import serializers
from .. import models

class MeetingListApiView (ListAPIView):
    model = models.Meeting
    serializer_class = serializers.MeetingSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
