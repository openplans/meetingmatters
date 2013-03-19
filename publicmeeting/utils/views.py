from rest_framework import views
from rest_framework.response import Response

from . import geocode

class GeoAutocomplete (views.APIView):
    def get(self, request, *args, **kwargs):
        string = request.GET.get('string', '')
        if string == '':
            return []

        possibilities = geocode.possibilities(string)
        return Response(possibilities)
