import requests
import argparse
import datetime
import json

'''
user send his flight parameters 
for example: --date 2018-04-13 --from BCN --to DUB --one-way
'''
parser = argparse.ArgumentParser(description='Kiwi weekend.')
parser.add_argument('--from', required=True)
parser.add_argument('--to', required=True)
parser.add_argument('--date', required=True)
parser.add_argument('--one-way', action='store_true')
parser.add_argument('--cheapest', action='store_true')
parser.add_argument('--shortest', action='store_true')
parser.add_argument('--fastest', action='store_true')
parser.add_argument('--return', action='store_true')
parser.add_argument('--bags')

args = vars(parser.parse_args())

'''
create a dict with values from user's param
'''
check_flight = {'flyFrom': None,
                'to': None,
                'dateFrom': None,
                'dateTo': None,
                'daysInDestinationFrom': None,
                'sort': None,
                'typeFlight': None,
                'bags': None
                }

days = datetime.datetime.strptime(args['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
check_flight['dateFrom'] = days
check_flight['typeFlight'] = 'oneway'
check_flight['sort'] = 'price'
check_flight['bags'] = args['bags']


def check_args(check_flight):
    '''

    :param check_flight: 
    :return: json with parsed param
    '''
    if args['one_way']:
        check_flight['typeFlight'] = 'oneway'

    if args['bags'] == None:
        check_flight['bags'] = 0

    check_flight['flyFrom'] = args['from']
    check_flight['to'] = args['to']

    if args['shortest'] or args['fastest']:
        check_flight['sort'] = 'duration'

    if args['return']:
        check_flight['typeFlight'] = 'round'

    if check_flight['typeFlight'] == 'round':
        check_flight['daysInDestinationFrom'] = args['return']
        check_flight['typeFlight'] = None
    return check_flight


check_args(check_flight)

# print(check_flight)

r = requests.get('https://api.skypicker.com/flights', params=check_flight)
flight = r.json()['data'][0]

# booking of the flight

url = 'http://128.199.48.38:8080/booking'

information = {
    "passengers": [
        {
            "firstName": "Kaja",
            "birthday": "1901-12-12",
            "lastName": "test",
            "title": "Mr",
            "documentID": "bla bla bla bla",
            "email": "kecyprdbedary@ihatemonday.com",

        }
    ],
    "currency": "EUR",
    "booking_token": flight['booking_token'],
    "bags": check_flight['bags']
}
print(information)
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(information), headers=headers)
print(r.json())
print("Hurray we found your flight! Only for " + str(flight['price']) + " EUR and remember the id of reservation "
      + str(r.json()['pnr']) + "!!!!!!!!")

