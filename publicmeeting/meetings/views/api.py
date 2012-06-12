from djangorestframework import views, mixins
from .. import resources

class MeetingListApiView (mixins.PaginatorMixin, views.ListModelView):
    resource = resources.MeetingResource
