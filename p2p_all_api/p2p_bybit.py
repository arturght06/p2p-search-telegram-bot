import requests, json
from pprint import pprint
import asyncio
import aiohttp

list_payments = {
    'monobank': 43,
    'a-bank': 1,
    'alipay': 2,
    'wechat': 3,
    '7-eleven': 4,
    'advcash': 5,
    'airtelmoney': 6,
    'airtm': 7,
    'aliorbank': 9,
    'applepay':10,
    'bankofgeorgia': 11,
    
    'wise': 78,
    'raiffeisenbankaval': 63,
    'pumb': 61,
    'privatbank': 60,
    'banktransfer': 14,
    }

async def p2p_bybit(s1, s2, buy_sell, *arr):
    list_reverse = dict(zip(list_payments.values(), list_payments.keys()))

    if len(arr) == 0:
        payTypes = ''
        transAmount = ''
    elif len(arr) == 1:
        if str(arr[0]).isdigit():
            payTypes = ''
            transAmount = arr[0]
        else:
            payTypes = arr[0]
            transAmount = ''
    elif len(arr) == 2:
        if str(arr[0]).isdigit():
            payTypes = arr[1]
            transAmount = arr[0]
        else:
            payTypes = arr[0]
            transAmount = arr[1]
            
    if payTypes != '':
        try:
            payTypes = list_payments[payTypes.lower().replace(' ', '')]
        except:
            return False
        
    cookies = {
        '_gcl_au': '1.1.2040385648.1656002726',
        '_ga': 'GA1.2.676111258.1656002726',
        '_gid': 'GA1.2.986525913.1656002726',
        '_by_l_g_d': '2a683512-b5ac-9905-2de8-058d3e2cdcb5',
        '_ym_d': '1656002727',
        '_ym_uid': '1656002727856920374',
        'b_t_c_k': '',
        '_abck': '6A7C8D541FA91655096622A74FADF444~0~YAAQZ717XOpjF5OBAQAA5IsSlgjnOZN+Cr0sJeVO/ZfLF5baXpezvA1Be0yqD3EWfV9xFZADVsCk/Db3sh8fvTVQdGcU72bKfqNrY3pET8z1PPuW/rCrJrIyl8+Vi8G9XmOVPahm4pcY+QNDfmx7yPvC4T6UAAn2dHNdD9iVE+F2kREhgp9mkfIFQAiAxY63ev78uEu7aQPr8eix29IcSDigODXLbGKWJTVv4Ank6b78bPcXjbrMnTxMy2wvrXRU9iQxN4pofEQrTvrwDiIS1K9hy1fvYBOTTX7jQlyt6xeS6K0MT4qDbj6qjs9GrPRwf3lk+mdOdeQm3twrt2CFPG9DX3mz0tqVC50C7Pj5SIDI5Iy5auOUHnldNstKQ4Kh/GgZm1ty8uQgkn+WgTtqiv4ufMsXICc=~-1~-1~-1',
        'bm_sz': '93F628E3B1DC9654FE72CF7F95F4E92A~YAAQZ717XO1jF5OBAQAA5IsSlhAx5MaibDlILf4K6VIbO/k86pOd1eJmtD90y4QXg8TgAf7jg2vZ3N22iTLpJfqwzQNbjvq5w2AxTMCRxX6zU3armwOzgRNkcVD1ma3R+MS/ODcWa4r/W7PTc+H2+G7SJRBt9KEZbmL8GcT2TiQTqI/F3gMaO20cMVsxTm6BXJlhrvVAtPUNqn6qsPD9vPWWWP7ZY9crIXw6maD1aOn4LGq1jeDMSuUB2c+m3Wap9MyTcDD3gHFzGqKHzv/msEkwQkR8SlU1xbwE3hp+sTgW/g==~3163186~3293488',
        'BYBIT_REG_REF_prod': '{"lang":"ru","g":"2a683512-b5ac-9905-2de8-058d3e2cdcb5","medium":"direct","url":"https://www.bybit.com/fiat/trade/otc/?actionType=0&token=USDT&fiat=UAH&paymentMethod=5"}',
        'bm_mi': '85DF33BE61916B08DA37969225C2132C~YAAQZ717XCBkF5OBAQAAzpASlhDh1Wknr/pu01b4LCjRUiH4oEUwFgH12GNupJeQTFvqi8GFo+ilICkGTrX4XPTOIYmqGFM46p69iv/RS2rwJFnAJSPJrVKbDbyS/pv2OUEH18Si+rbwJK25xSQN27MKz2/3nqi/UEl492bGqWN4DOWj6b4Y0XQJ4Vm+VYCI2ox4Nqsa655p+8ddxd/hKLXx0y6SyGjHWqzDrwcVA9BTDA7BgwlRZOh6yWgVfpBPUAuqw7uxeim5lS/M8sqN68oyBoojsOtJI+FHIThvBB+f9rsMGlYWs0+793TkUG06Afgf2iuWfJ9H1cqN+o8LFQ0s89ajfalc6yz71JtTawVfCLc=~1',
        '_ym_isad': '1',
        '_cc_id': 'c8e2123ef329a1f7afe030fc5b5f9def',
        'panoramaId_expiry': '1656166609166',
        'ak_bmsc': 'BFA012EFAC3B3DECBD2937608FCAFA8A~000000000000000000000000000000~YAAQZ717XExkF5OBAQAA4JUSlhB67i1Tz187XlweHP62Fs0Ljg91TmEdMcfZog9uuccANydeUh4WNT7ii9pPbb2bXZpYUU33cHuHY+FnvNqFUeb5evZO4GDzxX3ct1Uv4ooxssCGncpet7bTvoqh+pWLC5RJ2hO/n0RdiGjzRTX8/34XpBw1ABgjJ2AN+5xtfUhBS5bSZdQa3FkwPh/LNPklGsLcMKeviwdiItT43qjfc+hY7TtOYuPIocMx+YrLp4d6UcOBA1dYShMxithd6BGxR6TxtW1rs/E1akW7OkEmXXGJkmhB2q4FDjU474KHVsV65wz9G2buEWYVM8qa1/WsGCrV5JO+oxDiwh4LG3YbADO45X9hm+zSWUpDW3+4weVXzeTr04eMwoxWj8Qt1hFH2QNPqu2C0cm2BrOfpGON2OkFz/3raLC0sE7IoeY7Xv5/2/4n+Tg+9NVlgrtEGig3kOkaV8lNeWMFi9L9EdxwTpDXkyPfm8fn3vRrZnjpqjqIWWh0lyzyS7bu/ssFOtkm2xd48I209dn1WkImw8td7C0tnWTH',
        'bm_sv': '05391E9CBB6230187A40C2EDF26AE659~YAAQDgxAFzGCqDqBAQAAyHsXlhDCYz3hPQPEgJ6t4g9ucAZhwt+5vlV1mguipYpI7dIbTBQhZOESe39sHLdbW/RVueprR8d6XOTNrXBKLnNFz4MEIdb8Xfpa2sUibvBTn5b8qf/M62daz9K2xjAySmqpvyHxPgVk4uDnl9Tmq3h0CVN7dITKg8LhF3M8fEfABBZnS4lgjN/UwipZBVrKOJvXsxhU+ORm0Hnwp62+EAHNcTnTzBKk5z9rMK/4hbYn~1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22181917448ee6d3-0c629b7f0d46298-26021b51-1310720-181917448ef7e2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22_a_u_v%22%3A%220.0.5%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxOTE3NDQ4ZWU2ZDMtMGM2MjliN2YwZDQ2Mjk4LTI2MDIxYjUxLTEzMTA3MjAtMTgxOTE3NDQ4ZWY3ZTIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22181917448ee6d3-0c629b7f0d46298-26021b51-1310720-181917448ef7e2%22%7D',
        'RT': '"z=1&dm=bybit.com&si=ed5e034d-83de-49f6-b9b7-a85e076f5a0c&ss=l4sje9vc&sl=0&tt=0&rl=1"',
    }

    headers = {
        'authority': 'api2.bybit.com',
        'accept': 'application/json',
        'accept-language': 'ru',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_gcl_au=1.1.2040385648.1656002726; _ga=GA1.2.676111258.1656002726; _gid=GA1.2.986525913.1656002726; _by_l_g_d=2a683512-b5ac-9905-2de8-058d3e2cdcb5; _ym_d=1656002727; _ym_uid=1656002727856920374; b_t_c_k=; _abck=6A7C8D541FA91655096622A74FADF444~0~YAAQZ717XOpjF5OBAQAA5IsSlgjnOZN+Cr0sJeVO/ZfLF5baXpezvA1Be0yqD3EWfV9xFZADVsCk/Db3sh8fvTVQdGcU72bKfqNrY3pET8z1PPuW/rCrJrIyl8+Vi8G9XmOVPahm4pcY+QNDfmx7yPvC4T6UAAn2dHNdD9iVE+F2kREhgp9mkfIFQAiAxY63ev78uEu7aQPr8eix29IcSDigODXLbGKWJTVv4Ank6b78bPcXjbrMnTxMy2wvrXRU9iQxN4pofEQrTvrwDiIS1K9hy1fvYBOTTX7jQlyt6xeS6K0MT4qDbj6qjs9GrPRwf3lk+mdOdeQm3twrt2CFPG9DX3mz0tqVC50C7Pj5SIDI5Iy5auOUHnldNstKQ4Kh/GgZm1ty8uQgkn+WgTtqiv4ufMsXICc=~-1~-1~-1; bm_sz=93F628E3B1DC9654FE72CF7F95F4E92A~YAAQZ717XO1jF5OBAQAA5IsSlhAx5MaibDlILf4K6VIbO/k86pOd1eJmtD90y4QXg8TgAf7jg2vZ3N22iTLpJfqwzQNbjvq5w2AxTMCRxX6zU3armwOzgRNkcVD1ma3R+MS/ODcWa4r/W7PTc+H2+G7SJRBt9KEZbmL8GcT2TiQTqI/F3gMaO20cMVsxTm6BXJlhrvVAtPUNqn6qsPD9vPWWWP7ZY9crIXw6maD1aOn4LGq1jeDMSuUB2c+m3Wap9MyTcDD3gHFzGqKHzv/msEkwQkR8SlU1xbwE3hp+sTgW/g==~3163186~3293488; BYBIT_REG_REF_prod={"lang":"ru","g":"2a683512-b5ac-9905-2de8-058d3e2cdcb5","medium":"direct","url":"https://www.bybit.com/fiat/trade/otc/?actionType=0&token=USDT&fiat=UAH&paymentMethod=5"}; bm_mi=85DF33BE61916B08DA37969225C2132C~YAAQZ717XCBkF5OBAQAAzpASlhDh1Wknr/pu01b4LCjRUiH4oEUwFgH12GNupJeQTFvqi8GFo+ilICkGTrX4XPTOIYmqGFM46p69iv/RS2rwJFnAJSPJrVKbDbyS/pv2OUEH18Si+rbwJK25xSQN27MKz2/3nqi/UEl492bGqWN4DOWj6b4Y0XQJ4Vm+VYCI2ox4Nqsa655p+8ddxd/hKLXx0y6SyGjHWqzDrwcVA9BTDA7BgwlRZOh6yWgVfpBPUAuqw7uxeim5lS/M8sqN68oyBoojsOtJI+FHIThvBB+f9rsMGlYWs0+793TkUG06Afgf2iuWfJ9H1cqN+o8LFQ0s89ajfalc6yz71JtTawVfCLc=~1; _ym_isad=1; _cc_id=c8e2123ef329a1f7afe030fc5b5f9def; panoramaId_expiry=1656166609166; ak_bmsc=BFA012EFAC3B3DECBD2937608FCAFA8A~000000000000000000000000000000~YAAQZ717XExkF5OBAQAA4JUSlhB67i1Tz187XlweHP62Fs0Ljg91TmEdMcfZog9uuccANydeUh4WNT7ii9pPbb2bXZpYUU33cHuHY+FnvNqFUeb5evZO4GDzxX3ct1Uv4ooxssCGncpet7bTvoqh+pWLC5RJ2hO/n0RdiGjzRTX8/34XpBw1ABgjJ2AN+5xtfUhBS5bSZdQa3FkwPh/LNPklGsLcMKeviwdiItT43qjfc+hY7TtOYuPIocMx+YrLp4d6UcOBA1dYShMxithd6BGxR6TxtW1rs/E1akW7OkEmXXGJkmhB2q4FDjU474KHVsV65wz9G2buEWYVM8qa1/WsGCrV5JO+oxDiwh4LG3YbADO45X9hm+zSWUpDW3+4weVXzeTr04eMwoxWj8Qt1hFH2QNPqu2C0cm2BrOfpGON2OkFz/3raLC0sE7IoeY7Xv5/2/4n+Tg+9NVlgrtEGig3kOkaV8lNeWMFi9L9EdxwTpDXkyPfm8fn3vRrZnjpqjqIWWh0lyzyS7bu/ssFOtkm2xd48I209dn1WkImw8td7C0tnWTH; bm_sv=05391E9CBB6230187A40C2EDF26AE659~YAAQDgxAFzGCqDqBAQAAyHsXlhDCYz3hPQPEgJ6t4g9ucAZhwt+5vlV1mguipYpI7dIbTBQhZOESe39sHLdbW/RVueprR8d6XOTNrXBKLnNFz4MEIdb8Xfpa2sUibvBTn5b8qf/M62daz9K2xjAySmqpvyHxPgVk4uDnl9Tmq3h0CVN7dITKg8LhF3M8fEfABBZnS4lgjN/UwipZBVrKOJvXsxhU+ORm0Hnwp62+EAHNcTnTzBKk5z9rMK/4hbYn~1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22181917448ee6d3-0c629b7f0d46298-26021b51-1310720-181917448ef7e2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22_a_u_v%22%3A%220.0.5%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxOTE3NDQ4ZWU2ZDMtMGM2MjliN2YwZDQ2Mjk4LTI2MDIxYjUxLTEzMTA3MjAtMTgxOTE3NDQ4ZWY3ZTIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22181917448ee6d3-0c629b7f0d46298-26021b51-1310720-181917448ef7e2%22%7D; RT="z=1&dm=bybit.com&si=ed5e034d-83de-49f6-b9b7-a85e076f5a0c&ss=l4sje9vc&sl=0&tt=0&rl=1"',
        'guid': '2a683512-b5ac-9905-2de8-058d3e2cdcb5',
        'lang': 'ru',
        'origin': 'https://www.bybit.com',
        'platform': 'PC',
        'referer': 'https://www.bybit.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    if buy_sell.upper() == 'BUY':
        buy_sell = '1'
    elif buy_sell.upper() == 'SELL':
        buy_sell = '0'
    else:
        return False
        
    data = {
        'userId': '',
        'tokenId': s1.upper(),
        'currencyId': s2.upper(),
        'payment': payTypes,
        'side': buy_sell,
        'size': '10',
        'page': '1',
        'amount': '1000',
    }
    if transAmount != None:
        data['amount'] = transAmount

    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.post(f'https://api2.bybit.com/spot/api/otc/item/list', data=data) as resp:
            content = await resp.content.read()
            json_req = json.loads(content)
            try:
                data = json_req['result']['items']
                result_all = []
                for i in range(len(data)):
                    price = data[i]['price']
                    amount = data[i]['lastQuantity']
                    minAmount = data[i]['minAmount']
                    dynamicMaxAmount = data[i]['maxAmount']

                    tradeMethods = data[i]['payments']
                    methods = ''
                    for t in range(0, len(tradeMethods)):
                        if int(tradeMethods[t]) in list_reverse:
                            trade_method = list_reverse[tradeMethods[t]]
                        else:
                            trade_method = 'None'
                          
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
                    await session.close()
                    return result_all
            except:
                await session.close()
                return False

# resp = p2p_bybit('usdt', 'uah', 'bu', 'Monobank')
# if resp == False:
#     print('False')
# else:
#     print(resp)
