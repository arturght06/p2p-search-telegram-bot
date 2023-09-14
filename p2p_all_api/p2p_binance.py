import requests, json
import asyncio
import aiohttp
# import time

async def p2p_binance(s1, s2, buy_sell, *arr):
    # start = time.time()
    if len(arr) == 0:
        payTypes = []
        transAmount = None
    elif len(arr) == 1:
        if str(arr[0]).isdigit():
            transAmount = arr[0]
            payTypes = []
        elif arr[0] == '':
            payTypes = []
            transAmount = None
        else:
            payTypes = [arr[0]]
            transAmount = None
    elif len(arr) == 2:
        if str(arr[0]).isdigit():
            transAmount = arr[0]
            payTypes = [arr[1]]
        elif arr[0] == '':
            payTypes = []
            transAmount = None
        else:
            transAmount = arr[1]
            payTypes = [arr[0]]

    if payTypes != []:
        try:
            payTypes = [str(payTypes[0]).lower().replace(' ', '')]
        except:
            return False

    # headers = {
    #     'authority': 'p2p.binance.com',
    #     'accept': '*/*',
    #     'accept-language': 'ru,en-UA;q=0.9,en;q=0.8,ru-UA;q=0.7,en-US;q=0.6,uk;q=0.5,pl;q=0.4',
    #     'bnc-uuid': 'c43c2153-10fd-42cd-9513-e968e7f55c89',
    #     'c2ctype': 'c2c_merchant',
    #     'clienttype': 'web',
    #     # Already added when you pass json=
    #     # 'content-type': 'application/json',
    #     # Requests sorts cookies= alphabetically
    #     # 'cookie': 'cid=jHQ9Bjri; bnc-uuid=c43c2153-10fd-42cd-9513-e968e7f55c89; _gcl_au=1.1.669340651.1654327415; _ga=GA1.2.9842540.1654327416; BNC_FV_KEY=33ac9fc9ea53a28aae98b17bce82dbcb8c656590; OptanonAlertBoxClosed=2022-06-04T07:23:41.550Z; source=referral; campaign=www.binance.com; se_gd=BYXU1BQkBRQBgYEQLUhNgZZVhCBkTBZUFUGBdUk91VXUQVlNXVYX1; se_gsd=Yy42CityNjMjMAkhN1UhIDo9CVxRAgcGUF1DUVNXVlVRDVNS1; BNC-Location=; userPreferredCurrency=USD_USD; pl-id=114644299; se_sd=FUPCVWhsRFBClAawQGlAgZZHgDhoQEYVlRUVcWkV1RQVAC1NXVQU1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22114644299%22%2C%22first_id%22%3A%221812d9916297d8-086a9388285d72-26021b51-1310720-1812d99162a688%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221812d9916297d8-086a9388285d72-26021b51-1310720-1812d99162a688%22%7D; sys_mob=no; videoViewed=yes; isAccountsLoggedIn=y; logined=y; __BNC_USER_DEVICE_ID__={"c9c75df5e5146d4c7ef5e77fd3187e1a":{"date":1655558656936,"value":"1655558655889X13kEVc5D77VqVVDmfI"}}; p20t=web.114644299.6133CC18547D70F3F5BDC0F6866FF32B; fiat-prefer-currency=USD; noticeCache={"USD":true}; lang=uk-ua; futures-layout=pro; BNC_FV_KEY_EXPIRE=1655999991345; _gid=GA1.2.1933762390.1655913607; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+22+2022+19%3A42%3A02+GMT%2B0300+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.34.0&isIABGlobal=false&hosts=&consentId=fd9f6718-2f94-4f13-b40f-077a47970827&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=UA%3B30&AwaitingReconsent=false; _uetsid=6371df50f24411ec8718e1ab74e2344d; _uetvid=76b702d0e3d711ec970be11b8061b733; showBlockMarket=false; common_fiat=UAH',
    #     'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
    #     'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjEyODAsMTAyNCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6Ijk4NCwxMjgwIiwic3lzdGVtX3ZlcnNpb24iOiJXaW5kb3dzIDEwIiwiYnJhbmRfbW9kZWwiOiJ1bmtub3duIiwic3lzdGVtX2xhbmciOiJydSIsInRpbWV6b25lIjoiR01UKzMiLCJ0aW1lem9uZU9mZnNldCI6LTE4MCwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDIuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImxpc3RfcGx1Z2luIjoiUERGIFZpZXdlcixDaHJvbWUgUERGIFZpZXdlcixDaHJvbWl1bSBQREYgVmlld2VyLE1pY3Jvc29mdCBFZGdlIFBERiBWaWV3ZXIsV2ViS2l0IGJ1aWx0LWluIFBERiIsImNhbnZhc19jb2RlIjoiYTQwZGRhMzIiLCJ3ZWJnbF92ZW5kb3IiOiJHb29nbGUgSW5jLiAoTlZJRElBKSIsIndlYmdsX3JlbmRlcmVyIjoiQU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgUlRYIDMwNjAgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSkiLCJhdWRpbyI6IjEyNC4wNDM0NzUyNzUxNjA3NCIsInBsYXRmb3JtIjoiV2luMzIiLCJ3ZWJfdGltZXpvbmUiOiJFdXJvcGUvS2lldiIsImRldmljZV9uYW1lIjoiQ2hyb21lIFYxMDIuMC4wLjAgKFdpbmRvd3MpIiwiZmluZ2VycHJpbnQiOiIxYTgxYjAzNTQyYzc5MmVmNDcyN2M2YmNiMjllYTYzMiIsImRldmljZV9pZCI6IiIsInJlbGF0ZWRfZGV2aWNlX2lkcyI6IjE2NTU1NTg2NTU4ODlYMTNrRVZjNUQ3N1ZxVlZEbWZJIn0=',
    #     'fvideo-id': '33ac9fc9ea53a28aae98b17bce82dbcb8c656590',
    #     'lang': 'en',
    #     'origin': 'https://p2p.binance.com',
    #     'referer': 'https://p2p.binance.com/en/trade/Monobank/USDT?fiat=UAH',
    #     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    #     'x-trace-id': '8dde8969-c4a2-4e40-a0da-bf04dd21f723',
    #     'x-ui-request-trace': '8dde8969-c4a2-4e40-a0da-bf04dd21f723',
    # }

    json_data = {
        'page': 1,
        'rows': 10,
        'payTypes': payTypes,
        'countries': [],
        'publisherType': None,
        'transAmount': '',
        'asset': s1,
        'fiat': s2,
        'tradeType': buy_sell,

    }

    # cookies = {
    #     'cid': 'jHQ9Bjri',
    #     'bnc-uuid': 'c43c2153-10fd-42cd-9513-e968e7f55c89',
    #     '_gcl_au': '1.1.669340651.1654327415',
    #     '_ga': 'GA1.2.9842540.1654327416',
    #     'BNC_FV_KEY': '33ac9fc9ea53a28aae98b17bce82dbcb8c656590',
    #     'OptanonAlertBoxClosed': '2022-06-04T07:23:41.550Z',
    #     'source': 'referral',
    #     'campaign': 'www.binance.com',
    #     'se_gd': 'BYXU1BQkBRQBgYEQLUhNgZZVhCBkTBZUFUGBdUk91VXUQVlNXVYX1',
    #     'se_gsd': 'Yy42CityNjMjMAkhN1UhIDo9CVxRAgcGUF1DUVNXVlVRDVNS1',
    #     'BNC-Location': '',
    #     'userPreferredCurrency': 'USD_USD',
    #     'pl-id': '114644299',
    #     'se_sd': 'FUPCVWhsRFBClAawQGlAgZZHgDhoQEYVlRUVcWkV1RQVAC1NXVQU1',
    #     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22114644299%22%2C%22first_id%22%3A%221812d9916297d8-086a9388285d72-26021b51-1310720-1812d99162a688%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221812d9916297d8-086a9388285d72-26021b51-1310720-1812d99162a688%22%7D',
    #     'sys_mob': 'no',
    #     'videoViewed': 'yes',
    #     'isAccountsLoggedIn': 'y',
    #     'logined': 'y',
    #     '__BNC_USER_DEVICE_ID__': '{"c9c75df5e5146d4c7ef5e77fd3187e1a":{"date":1655558656936,"value":"1655558655889X13kEVc5D77VqVVDmfI"}}',
    #     'p20t': 'web.114644299.6133CC18547D70F3F5BDC0F6866FF32B',
    #     'fiat-prefer-currency': 'USD',
    #     'noticeCache': '{"USD":true}',
    #     'lang': 'uk-ua',
    #     'futures-layout': 'pro',
    #     'BNC_FV_KEY_EXPIRE': '1655999991345',
    #     '_gid': 'GA1.2.1933762390.1655913607',
    #     'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Jun+22+2022+19%3A42%3A02+GMT%2B0300+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.34.0&isIABGlobal=false&hosts=&consentId=fd9f6718-2f94-4f13-b40f-077a47970827&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=UA%3B30&AwaitingReconsent=false',
    #     '_uetsid': '6371df50f24411ec8718e1ab74e2344d',
    #     '_uetvid': '76b702d0e3d711ec970be11b8061b733',
    #     'showBlockMarket': 'false',
    #     'common_fiat': 'UAH',
    # }

    

    if transAmount != None:
        json_data['transAmount'] = transAmount

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=json_data) as resp:
            content = await resp.content.read()
            
            json_req = json.loads(content)
            #pprint(json_req['data'])
            try:
                data = json_req['data']
                result_all = []
                for i in range(len(data)):
                    price = data[i]['adv']['price']
                    amount = data[i]['adv']['tradableQuantity']
                    minAmount = data[i]['adv']['minSingleTransAmount']
                    dynamicMaxAmount = data[i]['adv']['dynamicMaxSingleTransAmount']

                    tradeMethods = data[i]['adv']['tradeMethods']
                    methods = ''
                    for t in range(0, len(tradeMethods)):
                        trade_method = tradeMethods[t]['tradeMethodShortName']
                        if trade_method == None:
                            trade_method = tradeMethods[t]['tradeMethodName']
                            
                        if t == len(tradeMethods)-1:
                            methods += trade_method
                        else:
                            methods += trade_method + ', '
                    
                    result_one = [price, amount, minAmount, dynamicMaxAmount, methods]
                    result_all.append(result_one)
                if len(result_all) == 0:
                    await session.close()
                    return False
                else:
                    # print('binance_time:',start - time.time())
                    await session.close()
                    return result_all
            except:
                await session.close()
                return False




        
    

# resp = p2p_binance('usdt', 'uah', 'buy', 'monobank')
# if resp == False:
#     print('False')
# else:
#     print(resp[0])
