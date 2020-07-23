"""
scraper.py 'ISB' 'KHI' 2020-07-24 2020-07-28

"""
import datetime
import requests
from lxml import html

# import sys

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0)'
                          ' Gecko/20100101 Firefox/78.0'})
URL = 'https://www.airblue.com/bookings/flight_selection.aspx'
params = {'TT': 'RT', 'SS': '', 'RT': '', 'DC': '', 'AC': '',
          'AM': '', 'AD': '',
          'RM': '', 'RD': '',
          'FL': '', 'CC': 'Y', 'CD': '', 'PA': '1', 'PC': '', 'PI': ''}
cities = {'AUH': 'Abu Dhabi',
          'DXB': 'Dubai',
          'ISB': 'Islamabad',
          'JED': 'Jeddah',
          'KHI': 'Karachi',
          'LHE': 'Lahore',
          'MUX': 'Multan',
          'PEW': 'Peshawar',
          'RUH': 'Riyadh',
          'SHJ': 'Sharjah'}


class FlightSelection:
    """
      Flight Selection
    """

    def __init__(self, departure_city, arrival_city, date1, date2=''):
        self.d_city = departure_city
        self.a_city = arrival_city
        self.a_date = date1
        self.r_date = date2

    @staticmethod
    def is_correct(date):
        """
         Checking the correctness of the date
        :param date: string in format dd-mm-yyyy
        :return: datetime.date()
        """
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            today = datetime.datetime.today().date()
            if date < today:
                print('This date is overdue! Unable to process flight search. '
                      'Please select today or a future date for travel.')
                return None
            return date
        except ValueError:
            print('Invalid date!')
            return None

    def is_valid(self):
        """
        Checking the correctness of the entered data
        :return:
        """
        while self.d_city not in cities.keys():
            print('IATA code from where you will fly is not correct')
            self.d_city = input('Input IATA code from where you will fly:')
        while self.a_city not in cities.keys():
            print('IATA code where you will fly is not correct')
            self.a_city = input('Input IATA code where you will fly:')
        self.a_date = self.is_correct(self.a_date)
        while not self.a_date:
            self.a_date = input('Input departure date in format yyyy-mm-dd:')
            self.a_date = self.is_correct(self.a_date)
        if self.r_date:
            self.r_date = self.is_correct(self.r_date)
            while not self.r_date:
                self.r_date = input('Input return date in format yyyy-mm-dd:')
                self.r_date = self.is_correct(self.r_date)

    def fill_in_params(self):
        """
        fill in dict values
        :return:
        """
        params['DC'] = self.d_city
        params['AC'] = self.a_city
        params['AM'] = self.a_date.strftime("%Y-%m")
        params['AD'] = self.a_date.strftime("%d")
        if self.r_date:
            params['TT'] = 'RT'
            params['RM'] = self.r_date.strftime("%Y-%m")
            params['RD'] = self.r_date.strftime("%d")
        else:
            params['TT'] = 'OW'


def get_html():
    """
    request get
    :return: response.text
    """
    response = requests.get(url=URL,
                            params=params,
                            headers=headers,
                            verify=False)
    print(response.url)
    if response.ok:
        return response.text
    print(response.status_code)
    return ''


def find_duration(depart, arrive):
    """
    find duration of flight
    :param depart:
    :param arrive:
    :return: datetime.timedelta
    """
    time1 = datetime.datetime.strptime(depart, '%I:%M %p')
    time2 = datetime.datetime.strptime(arrive, '%I:%M %p')
    difference = time2 - time1
    return difference


def unpacking_table(string, number, date):
    """
    Scrapes data from table
    :param string: html code
    :param number: number of table
    :param date: flight date
    :return: lisf of dict
    """
    result = []
    date = date.strftime("%Y_%m_%d")
    source_code = html.fromstring(string)
    tbodys = source_code.xpath('//table[@id = "trip_%s_date_%s"]/tbody'
                               % (number, date))
    # print("trip_%s_date_%s" % (number, date))
    for tbody in tbodys:
        tds = tbody.xpath('./tr/td')
        flight = tds[0].text_content().strip()
        depart = tds[1].text_content().strip()
        arrive = tds[3].text_content().strip()
        duration = find_duration(depart, arrive)
        try:
            value = tbody.xpath('./tr/td[@class="family family-EV '
                                'family-group-Y "]')[0]
            cost_value = value.xpath('./label/span/text()')[0].strip()
            currency_value = value.xpath('./label/span/b/text()')[0].strip()
        except IndexError:
            cost_value = currency_value = ''
        try:
            flexi = tbody.xpath('./tr/td[@class="family family-EF '
                                'family-group-Y "]')[0]
            cost_flexi = flexi.xpath('./label/span/text()')[0].strip()
            currency_flexi = flexi.xpath('./label/span/b/text()')[0].strip()
        except IndexError:
            cost_flexi = currency_flexi = ''

        try:
            xtra = tbody.xpath('./tr/td[@class="family family-EX '
                               'family-group-Y "]')[0]
            cost_xtra = xtra.xpath('./label/span/text()')[0].strip()
            currency_xtra = xtra.xpath('./label/span/b/text()')[0].strip()
        except IndexError:
            cost_xtra = currency_xtra = ''

        data = {
            'flight': flight,
            'depart': depart,
            'arrive': arrive,
            'duration': str(duration),
            'Value (No Bag)': [cost_value, currency_value],
            'Flexi (20 kg Bag)': [cost_flexi, currency_flexi],
            'Xtra (2 Bags 20kg Each)': [cost_xtra, currency_xtra],
        }
        result.append(data)
    return result


def main():
    """
    main function
    :return:
    """
    departure_city = 'ISB'  # sys.argv[1]
    arrival_city = "KHI"  # sys.argv[2]
    date1 = "2020-07-24"  # sys.argv[3]
    date2 = '2020-07-25'  # sys.argv[4]
    flight = FlightSelection(departure_city, arrival_city, date1, date2)
    # fs = FlightSelection(*sys.argv[1:])
    flight.is_valid()
    flight.fill_in_params()
    print(params)
    response = get_html()
    table1 = []
    table2 = []
    if response:
        if date1:
            table1 = unpacking_table(response, 1, flight.a_date)
        print(table1)
        if date2:
            table2 = unpacking_table(response, 2, flight.r_date)
        print(table2)
    else:
        print('No answer!')


if __name__ == '__main__':
    main()
