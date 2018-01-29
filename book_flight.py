import requests
import argparse
import datetime
import json
import time
import sys


def create_parser():
    '''
    take arguments from console input
    for example: --date 2018-04-13 --from BCN --to DUB --one-way
    :return: parser with data
    '''
    parser = argparse.ArgumentParser(description='Kiwi weekend.')
    parser.add_argument('--from', required=True, help='args support Airports (City) in IATA format')
    parser.add_argument('--to', required=True, help='args support Airports (City) in IATA format')
    parser.add_argument('--date', required=True, help='use format YYYY-MM-DD')
    parser.add_argument('--one-way', action='store_true', help='if you want to find one-way flight')
    parser.add_argument('--cheapest', action='store_true', help='if you want to find cheapest flight')
    parser.add_argument('--shortest', action='store_true', help='if you want to find shortest flight')
    parser.add_argument('--fastest', action='store_true', help='if you want to find fastest flight')
    parser.add_argument('--return', help='number with nights in destination, can be empty')
    parser.add_argument('--bags', help='if want some bags with you, can be empty')
    return parser

create_parser()
args = vars(create_parser().parse_args())
# print(args)

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
                'bags': None,
                'return': None,
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


'''
call the kiwi api with data from user
'''
try:
    r = requests.get('https://api.skypicker.com/flights', params=check_flight)
    flight = r.json()['data'][0]
except:
    print('uups, something is wrong :( , check if your data are correct')
    exit()



'''
url with 
'''
url = 'http://128.199.48.38:8080/booking'


'''
kiwi api needs to know some information about passenger, I created dummy one
'''
information = {
    "passengers": [
        {
            "firstName": "Milos",
            "birthday": "1901-12-12",
            "lastName": "Zeman",
            "title": "Mr",
            "documentID": "Su prezident, bleeee",
            "email": "zhradudoprdele@ovcacek.com",

        }
    ],
    "currency": "EUR",
    "booking_token": flight['booking_token'],
    "bags": check_flight['bags']
}
# print(information)
try:
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(information), headers=headers)

except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

# print(r.json())

'''
check if user wants some bag(s), price will be higher
'''
number_of_bags = len(flight['bags_price'])

if int(check_flight['bags']) != 0 and int(check_flight['bags']) <= number_of_bags:
        bag = (flight['bags_price'].get(check_flight['bags'])) + flight['price']
        a = ''

elif number_of_bags < int(check_flight['bags']):
    bag = flight['price']
    a = " Sorry, too much bags, you cannot take them all only " + str(number_of_bags) + "!!!!!!!! The price is for flight " \
                                                                                        "without any bags. "

else:
    bag = flight['price']
    a = ''

# print(datetime.datetime.utcfromtimestamp(flight['aTime']).strftime('%Y-%m-%dT%H:%M:%SZ'))
dtime = time.strftime("%D %H:%M", time.localtime(int(flight['dTimeUTC'])))
atime = time.strftime("%D %H:%M", time.localtime(int(flight['aTimeUTC'])))
print("Ok, so you wanna fly from " + str(flight['cityFrom']) + " to " + str(flight['cityTo'])
      + ", hm? Hurray we found your flight! Only for " + str(bag) + " EUR and remember the id of reservation "
      + str(r.json()['pnr']) +"." + a + "Your flight is departed at " + dtime + " in UTC time. Arrival time is " + atime + " in UTC time." )

