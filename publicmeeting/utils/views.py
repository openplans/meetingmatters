from djangorestframework import views

from . import geocode

class GeoAutocomplete (views.View):
    def get(self, request, *args, **kwargs):
        string = request.GET.get('string', '')
        if string == '':
            return []

        possibilities = geocode.possibilities(string)
        return possibilities
