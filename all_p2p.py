from p2p_all_api import p2p_binance, p2p_bybit
from pprint import pprint

async def infoOfAllExchanges(changing, s1, s2, buy_sell, *arr):
    if len(arr) == 0:
        binance = await p2p_binance.p2p_binance(s1, s2, buy_sell)
        bybit = await p2p_bybit.p2p_bybit(s1, s2, buy_sell)
        # huobi = await p2p_huobi.p2p_huobi(s1, s2, buy_sell)
    elif len(arr) == 1:
        binance = await p2p_binance.p2p_binance(s1, s2, buy_sell, arr[0])
        bybit = await p2p_bybit.p2p_bybit(s1, s2, buy_sell, arr[0])
        # huobi = await p2p_huobi.p2p_huobi(s1, s2, buy_sell, arr[0])
    elif len(arr) == 2:
        binance = await p2p_binance.p2p_binance(s1, s2, buy_sell, arr[0], arr[1])
        bybit = await p2p_bybit.p2p_bybit(s1, s2, buy_sell, arr[0], arr[1])
        # huobi = await p2p_huobi.p2p_huobi(s1, s2, buy_sell, arr[0], arr[1])

    result = f'💰{s1.upper()}/{s2.upper()}\n<i>Коротко...</i>\n'
        
        
    if changing == True:
        if binance != False:
            binance = binance[0]
        if bybit != False:
            bybit = bybit[0]
        # if huobi != False:
        #     huobi = huobi[0]

        all_exgs = [binance, bybit]
        all_names = ['Binance', 'Bybit']
        for i in range(len(all_exgs)):
            if all_exgs[i] == False:
                result += f'• {all_names[i]}: 〰\n'
            else:
                result += f'• {all_names[i]}: <b>{all_exgs[i][0]}</b>\n'
        result += '\n<i>Подробиці:</i>\n'
        for i in range(len(all_exgs)):
            if all_exgs[i] == False:
                result += f'🔹 {all_names[i]}: 〰 | Об’єм: 〰\nЛіміти: 〰-〰 | 〰〰〰〰\n'
            else:
                result += f'🔹 {all_names[i]}: <b>{all_exgs[i][0]}</b> | Об’єм: <b>{all_exgs[i][1]}</b>\nЛіміти: <b>{all_exgs[i][2]}</b>-<b>{all_exgs[i][3]}</b> | <i>{all_exgs[i][4]}</i>\n'
        return result       
    elif changing == False:
        return {'binance': binance, 'bybit': bybit}

async def infoOfAllExchanges_p2p_one(s1, s2, buy_sell, exchg, *arr):
    if len(arr) == 0:
        if exchg == 1:
            curr = await p2p_binance.p2p_binance(s1, s2, buy_sell)
        elif exchg == 3:
            curr = await p2p_bybit.p2p_bybit(s1, s2, buy_sell)
        # elif exchg == 2:
        #     curr = await p2p_huobi.p2p_huobi(s1, s2, buy_sell)
    elif len(arr) == 1:
        if exchg == 1:
            curr = await p2p_binance.p2p_binance(s1, s2, buy_sell, arr[0])
        elif exchg == 3:
            curr = await p2p_bybit.p2p_bybit(s1, s2, buy_sell, arr[0])
        # elif exchg == 2:
        #     curr = await p2p_huobi.p2p_huobi(s1, s2, buy_sell, arr[0])
    elif len(arr) == 2:
        if exchg == 1:
            curr = await p2p_binance.p2p_binance(s1, s2, buy_sell, arr[0], arr[1])
        elif exchg == 3:
            curr = await p2p_bybit.p2p_bybit(s1, s2, buy_sell, arr[0], arr[1])
        # elif exchg == 2:
        #     curr = await p2p_huobi.p2p_huobi(s1, s2, buy_sell, arr[0], arr[1])

    if exchg == 1:
        exchg = 'Binance'
    # elif exchg == 2:
    #     exchg = 'Huobi'
    elif exchg == 3:
        exchg = 'Bybit'

    result = f'📊{s1.upper()}/{s2.upper()}\n<i>Ордери на <b>{exchg}</b>:</i>\n\n'
    
    if curr != False:
        inx = 1
        for i in curr:
            result += f'🔹<i>{inx}.</i> Ціна: <b>{i[0]}</b> | Об’єм: <b>{i[1]}</b>\nЛіміти: <b>{i[2]}</b>-<b>{i[3]}</b> | <i>{i[4]}</i>\n'
            inx += 1
    else:
        result += '• Ціна: 〰 | Об’єм: 〰\nЛіміти: 〰-〰 | 〰〰〰〰\n'

    return result
    # if changing == True:
    #     if binance != False:
    #         binance = binance[0]
    #     if bybit != False:
    #         bybit = bybit[0]
    #     if huobi != False:
    #         huobi = huobi[0]

    #     all_exgs = [binance, bybit, huobi]
    #     all_names = ['Binance', 'Bybit', 'Huobi']
    #     for i in range(len(all_exgs)):
    #         if all_exgs[i] == False:
    #             result += f'📍{all_names[i]}: 〰\n'
    #         else:
    #             result += f'📍{all_names[i]}: <b>{all_exgs[i][0]}</b>\n'
    #     result += '\nПодробиці:\n'
    #     for i in range(len(all_exgs)):
    #         if all_exgs[i] == False:
    #             result += f'📌{all_names[i]}: 〰 | Об’єм: 〰\nЛіміти: 〰-〰 | 〰〰〰〰\n'
    #         else:
    #             result += f'📌{all_names[i]}: <b>{all_exgs[i][0]}</b> | Об’єм: <b>{all_exgs[i][1]}</b>\nЛіміти: <b>{all_exgs[i][2]}</b>-<b>{all_exgs[i][3]}</b> | <i>{all_exgs[i][4]}</i>\n'
    #     return result       
    # elif changing == False:
    #     return {'binance': binance, 'huobi': huobi, 'bybit': bybit}
        
    # except:
        # return False

# print(infoOfAllExchanges_p2p_one('usdt', 'uah', 1, 'Monobank'))
#def inStr_ioae()
