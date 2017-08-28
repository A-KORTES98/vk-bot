import requests
def getWeather(city) -> 'str':
    if city == '':
        city = 'Saint-Petersbyrg'
    s_city = city + ",RU"
    city_id = 0
    appid = "6f893c6d1f2c0f5bfff1a3d0175bae31"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
    except Exception as e:
        return "Specified city: '" + city + "' does not exist! Пёс собака"
        pass


    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        countPos = 0
        string = 'City: ' + ('Saint-Petersburg' if data['city']['name'] == 'Novaya Gollandiya' else data['city']['name']) + '\n\n'

        print (data)
        for i in data['list']:
            print(i)
            if countPos > 8:
                break
            date, cTime = i['dt_txt'].split(' ')

            string += date + ' | ' + cTime + ' | ' + \
                      '{0:+3.0f}'.format(i['main']['temp']) + \
                      ' ' + \
                      i['weather'][0]['description'] + ' | ветер: ' + \
                      '{0:3.0f}'.format(i['wind']['speed']) + ' м/c\n\n'
            countPos += 1
        return string
    except Exception as e:
        print("Exception (forecast):", e)
        pass
