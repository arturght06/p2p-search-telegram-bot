import json
import requests
from time import sleep
import asyncio
import aiohttp
import time

async def prices(symbol1, symbol2):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://api.binance.com/api/v1/ticker/24hr?symbol={symbol1.upper()}{symbol2.upper()}') as binance_resp:
                binance_json_req = json.loads(await binance_resp.text())
                binance_lastPrice = float(binance_json_req['lastPrice'])
        except:
            binance_lastPrice = 0
        print(binance_lastPrice)

        try:
            async with session.get(f'https://api.qmall.io/api/v1/public/ticker?market={symbol1.upper()}_{symbol2.upper()}') as qmall_resp:
                qmall_json_req = json.loads(await qmall_resp.text())
                qmall_lastPrice = float(qmall_json_req['result']['bid'])
        except:
            qmall_lastPrice = 0
        print(qmall_lastPrice)

        try:
            async with session.get(f'https://whitebit.com/api/v1/public/ticker?market={symbol1.upper()}_{symbol2.upper()}') as whitebit_resp:
                whitebit_json_req = json.loads(await whitebit_resp.text())
                whitebit_lastPrice = float(whitebit_json_req['result']['last'])
        except:
            whitebit_lastPrice = 0
        print(whitebit_lastPrice)

        try:
            async with session.get(f'https://api.huobi.pro/market/detail/merged?symbol={symbol1.lower()}{symbol2.lower()}') as huobi_resp:
                huobi_json_req = json.loads(await huobi_resp.text())
                huobi_lastPrice = float(huobi_json_req['tick']['close'])
        except:
            huobi_lastPrice = 0
        print(huobi_lastPrice)

        try:
            async with session.get(f'https://api.exmo.com/v1.1/ticker') as exmo_resp:
                exmo_json_req = json.loads(await exmo_resp.text())
                exmo_lastPrice = float(exmo_json_req[f'{symbol1.upper()}_{symbol2.upper()}']['buy_price'])
        except:
            exmo_lastPrice = 0
        print(exmo_lastPrice)

        try:
            async with session.get(f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol1.upper()}-{symbol2.upper()}') as kucoin_resp:
                kucoin_json_req = json.loads(await kucoin_resp.text())
                kucoin_lastPrice = float(kucoin_json_req['data']['price'])
        except:
            kucoin_lastPrice = 0
        print(kucoin_lastPrice)

        try:
            async with session.get(f'https://api.bybit.com/spot/quote/v1/depth?symbol={symbol1.upper()}{symbol2.upper()}') as bybit_resp:
                bybit_json_req = json.loads(await bybit_resp.text())
                bybit_lastPrice = float(bybit_json_req['result']['bids'][0][0])
        except:
            bybit_lastPrice = 0
        print(bybit_lastPrice)

        try:
            async with session.get(f'https://aws.okx.com/api/v5/market/ticker?instId={symbol1.upper()}-{symbol2.upper()}-SWAP') as okx_resp:
                okx_json_req = json.loads(await okx_resp.text())
                okx_lastPrice = float(okx_json_req['data'][0]['last'])
        except:
            okx_lastPrice = 0
        print(okx_lastPrice)

        try:
            async with session.get(f'https://api.kuna.io/v3/book/{symbol1.lower()}{symbol2.lower()}') as kuna_resp:
                kuna_json_req = json.loads(await kuna_resp.text())
                kuna_lastPrice = float(kuna_json_req[0][0])
        except:
            kuna_lastPrice = 0
        print(kuna_lastPrice)
        

        print('spot_time:',start - time.time())

        all_prices_array = {'kuna        ': kuna_lastPrice, 'okx           ': okx_lastPrice, 'bybit        ': bybit_lastPrice, 'kucoin     ': kucoin_lastPrice, 'binance   ': binance_lastPrice, 'qmall       ': qmall_lastPrice, 'whitebit  ': whitebit_lastPrice, 'exmo       ': exmo_lastPrice, 'huobi       ': huobi_lastPrice}
        # all_prices = {kucoin_lastPrice: 'kucoin', binance_lastPrice: 'binance', qmall_lastPrice: 'qmall', whitebit_lastPrice: 'whitebit', huobi_lastPrice: 'huobi', exmo_lastPrice: 'exmo'}
        all_prices = []
        for variable in sorted(all_prices_array.items(), key = lambda para: (para[1], para[0])):
            all_pric = {}
            #print(variable)
            key = variable[0]
            var = variable[1]
            all_pric[key] = var
            all_prices.append(all_pric)
        all_prices.reverse()

        if float((str(all_prices[0]).split(': ')[1])[:-1]) != 0 and float((str(all_prices[1]).split(': ')[1])[:-1]) == 0 or float((str(all_prices[0]).split(': ')[1])[:-1]) == 0:
            prc = None
        elif float((str(all_prices[-1]).split(': ')[1])[:-1]) == 0:
            f_market = (str(all_prices[0]).split('\'')[1]).split(' ')[0]

            frs_el = float((str(all_prices[0]).split(': ')[1])[:-1])
            indx = 0
            for pil in all_prices:
                if float((str(all_prices[indx]).split(': ')[1])[:-1]) != 0 and float((str(all_prices[indx + 1]).split(': ')[1])[:-1]) == 0:
                    end_el = float((str(all_prices[indx]).split(': ')[1])[:-1])
                    end_market = (str(all_prices[indx]).split('\'')[1]).split(' ')[0]
                indx+=1
            prc = str(round(((frs_el / end_el)*100)-100, 4))+'%'
        else:
            f_market = (str(all_prices[0]).split('\'')[1]).split(' ')[0]
            end_market = (str(all_prices[-1]).split('\'')[1]).split(' ')[0]

            frs_el = float((str(all_prices[0]).split(': ')[1])[:-1])
            end_el = float((str(all_prices[-1]).split(': ')[1])[:-1])
            prc = str(round(((frs_el / end_el)*100)-100, 4))+'%'



        # end_el = float((str(all_prices[-1]).split(': ')[1])[:-1])
        # if end_el and frs_el != 0:
        #     prc = str(round(((frs_el / end_el)*100)-100, 4))+'%'
        # else:
        #     prc = 0
        #print(prc)

        if prc == None:
            await session.close()
            return [all_prices, prc]
        elif prc != None:
            await session.close()
            return [all_prices, prc, f_market, end_market, frs_el, end_el]

#print(prices('Usdt', 'uah')[0])

async def pricesString(s1, s2, prices):
    allPric = await prices(s1, s2)
    allPrices = allPric[0]
    # print(allPrices)
    result = ''
    number = 0
    for i in allPrices:
        fillc=" "
        number += 1
        for t in i:
            if float(i.get(t)) != 0:
                result += f'• {t}: <b>{i.get(t)}</b>\n'
            else:
                result += f'• {t}: немає пари❄️\n'

    if allPric[1] != None:
        result += f'\n🔥Найбільший спред: <b>{allPric[1]}</b>\n👉Купуємо на <b>{str(allPric[3]).capitalize()}</b> по <b>{allPric[5]}</b>\n👈Продаємо на <b>{str(allPric[2]).capitalize()}</b> по <b>{allPric[4]}</b>'
    else:
        result += '\n💢Не можемо порахувати спред😞'
    return result
    
#print(pricesString('usdt', 'uah', prices))


async def price_Binance(symbol1, symbol2):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.binance.com/api/v1/ticker/24hr?symbol={symbol1}{symbol2}') as resp:
            print(resp.status)
            print(await resp.text())
            json_req = json.loads(await resp.text())
            lastPrice = round(float(json_req['lastPrice']), 3)
            await session.close()
            return lastPrice


def price_Qmall(symbol1, symbol2):
    resp = requests.get(f'https://api.qmall.io/api/v1/public/ticker?market={symbol1}_{symbol2}')
    json_req = json.loads(resp.text)
    lastPrice = round(float(json_req['result']['bid']), 3)
    return lastPrice

def price_WhiteBit(symbol1, symbol2):
    resp = requests.get(f'https://whitebit.com/api/v1/public/ticker?market={symbol1}_{symbol2}')
    json_req = json.loads(resp.text)
    lastPrice = round(float(json_req['result']['last']), 3)
    return lastPrice

def price_Huobi(symbol1, symbol2):
    resp = requests.get(f'https://api.huobi.pro/market/detail/merged?symbol={symbol1}{symbol2}')
    json_req = json.loads(resp.text)
    lastPrice = round(float(json_req['tick']['close']), 3)
    return lastPrice
