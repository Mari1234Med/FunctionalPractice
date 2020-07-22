import requests
import datetime
from lxml import html

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0)'
                          ' Gecko/20100101 Firefox/78.0'})
url = 'https://www.airblue.com/bookings/flight_selection.aspx'
params = {'TT': 'RT', 'SS': '', 'RT': '', 'DC': 'KHI', 'AC': 'ISB',
          'AM': '2020-07', 'AD': '24',
          'RM': '2020-07', 'RD': '25',
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


def get_html():
    response = requests.get(url=url,
                            params=params,
                            headers=headers,
                            verify=False)
    print(response.url)
    if response.ok:
        return response.text
    print(response.status_code)
    return ''


def find_duration(depart, arrive):
    time1 = datetime.datetime.strptime(depart, '%I:%M %p')
    time2 = datetime.datetime.strptime(arrive, '%I:%M %p')
    difference = time2 - time1
    return difference


def unpacking_table(string):
    result = []
    source_code = html.fromstring(string)
    tbodys = source_code.xpath('//table[@id = "trip_1_date_2020_07_24"]/tbody')
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
        except Exception:
            cost_value = currency_value = ''
        try:
            flexi = tbody.xpath('./tr/td[@class="family family-EF '
                                'family-group-Y "]')[0]
            cost_flexi = flexi.xpath('./label/span/text()')[0].strip()
            currency_flexi = flexi.xpath('./label/span/b/text()')[0].strip()
        except Exception:
            cost_flexi = currency_flexi = ''

        try:
            xtra = tbody.xpath('./tr/td[@class="family family-EX '
                               'family-group-Y "]')[0]
            cost_xtra = xtra.xpath('./label/span/text()')[0].strip()
            currency_xtra = xtra.xpath('./label/span/b/text()')[0].strip()
        except Exception:
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


def is_correct(date):
    # dd-mm-yyyy
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        valid_date = [date.strftime("%Y-%m"), date.strftime("%d")]
        today = datetime.datetime.today().date()
        if date < today:
            print('This date is overdue! Unable to process flight search. '
                  'Please select today or a future date for travel.')
            return None
        return valid_date
    except ValueError:
        print('Invalid date!')
        return None


def input_data(dc, ac, am_date, rm_date=''):
    while dc not in cities.keys():
        print('IATA code from where you will fly is not correct')
        dc = input('Input IATA code from where you will fly:')
    while ac not in cities.keys():
        print('IATA code where you will fly is not correct')
        ac = input('Input IATA code where you will fly:')
    am_date = is_correct(am_date)
    while not am_date:
        am_date = input('Input departure date in format dd-mm-yyyy:')
        am_date = is_correct(am_date)
    if rm_date:
        rm_date = is_correct(rm_date)
        while not rm_date:
            rm_date = input('Input return date in format dd-mm-yyyy:')
            rm_date = is_correct(rm_date)
        params['RM'] = rm_date[0]
        params['RD'] = rm_date[1]
    else:
        # полет в одну сторону
        pass
    params['DC'] = dc
    params['AC'] = ac
    params['AM'] = am_date[0]
    params['AD'] = am_date[1]


def main():
    # response = get_html(host + url, headers=headers)
    # source_code = html.fromstring(response)
    input_data("ISB", "KHI", "24-07-2020", "25-07-2020")
    print(params)

    data = unpacking_table(get_html())
    print(data)


if __name__ == '__main__':
    main()
