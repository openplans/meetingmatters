import json
import requests

def possibilities(partial_address):
    results = geocode(partial_address)['results']
    return [result['formatted_address'] for result in results]

def geocode(address, retries=5, service='google', **kwargs):
    """attempts to geocode an address"""

    if service == 'google':
        response = requests.get(
            'http://maps.googleapis.com/maps/api/geocode/json',
            params={'address': address, 'sensor': 'false'})

        if response.status_code != 200 and retries > 0:
            return geocode(address, retries-1)
        if response.status_code != 200:
            return None

        response.encoding = 'UTF8'
        return json.loads(response.text)

    else:
        raise ValueError('Unrecognized service: %s' % service)

#    elif service == 'yahoo':
#        response = requests.get(
#            'http://where.yahooapis.com/geocode',
#            params={'location': address, 'flags': 'J'})

#        if response.status_code != 200 and retries > 0:
#            return geocode(address, retries-1)
#        if response.status_code != 200:
#            return None

#        response.encoding = 'UTF8'
#        result = json.loads(response.text)

#        return results
#
