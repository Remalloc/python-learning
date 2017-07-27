# -*- coding:utf-8 -*-

from xml.parsers.expat import ParserCreate
import re

nowdays = None
week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def analyze_lable(attrs, result):
    def get_location():
        if not (attrs.get('city') and attrs.get('country')):
            return None
        result['city'] = attrs.get('city')
        result['country'] = attrs.get('country')
        return result

    def get_nowdays():
        global nowdays
        if not attrs.get('date') or nowdays:
            return None
        nowdays = re.split(',', attrs['date'])[0]
        result['nowdays'] = nowdays
        return result

    def get_today():
        if not (nowdays == attrs.get('day', -1)) or result.get('today'):
            return None
        today = {}
        today['text'] = attrs.get('text')
        today['low'] = int(attrs.get('low'))
        today['high'] = int(attrs.get('high'))
        result['today'] = today
        return result

    def get_tomorrow():
        if not (nowdays and attrs.get('day')) or result.get('tomorrow'):
            return None
        for i in range(len(week)):
            if week[i] == nowdays:
                if week[(i + 1) % len(week)] == attrs.get('day'):
                    break
        if i == len(week) - 1:
            return None
        tomorrow = {}
        tomorrow['text'] = attrs.get('text')
        tomorrow['low'] = int(attrs.get('low'))
        tomorrow['high'] = int(attrs.get('high'))
        result['tomorrow'] = tomorrow
        return result

    get_location()
    get_nowdays()
    get_today()
    get_tomorrow()
    return result


class WeatherSaxHandler(object):
    def __init__(self):
        self.flag = False
        self.result = {}

    def start_element(self, name, attrs):
        analyze_lable(attrs, self.result)

    def end_element(self, name):
        pass

    def char_data(self, text):
        pass

    def get_result(self):
        return self.result


def parse_weather(xml):
    handler = WeatherSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)

    return handler.get_result()


# 测试:
data = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
    <channel>
        <title>Yahoo! Weather - Beijing, CN</title>
        <lastBuildDate>Wed, 27 May 2015 11:00 am CST</lastBuildDate>
        <yweather:location city="Beijing" region="" country="China"/>
        <yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/>
        <yweather:wind chill="28" direction="180" speed="14.48" />
        <yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" />
        <yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/>
        <item>
            <geo:lat>39.91</geo:lat>
            <geo:long>116.39</geo:long>
            <pubDate>Wed, 27 May 2015 11:00 am CST</pubDate>
            <yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" />
            <yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" />
            <yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" />
            <yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" />
            <yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" />
            <yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" />
        </item>
    </channel>
</rss>
'''
weather = parse_weather(data)
assert weather['city'] == 'Beijing', weather['city']
assert weather['country'] == 'China', weather['country']
assert weather['today']['text'] == 'Partly Cloudy', weather['today']['text']
assert weather['today']['low'] == 20, weather['today']['low']
assert weather['today']['high'] == 33, weather['today']['high']
assert weather['tomorrow']['text'] == 'Sunny', weather['tomorrow']['text']
assert weather['tomorrow']['low'] == 21, weather['tomorrow']['low']
assert weather['tomorrow']['high'] == 34, weather['tomorrow']['high']
print('Weather:', str(weather))
