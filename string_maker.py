from all_p2p import infoOfAllExchanges
from api import prices
from pprint import pprint
import asyncio
import aiohttp

s1 = 'eth'
s2 = 'uah'
pay_type = 'monobank'
amount = ''
to_string = True

async def allP2Pprices(s1, s2, *arr):
    if len(arr) == 0:
        pay_type = ''
        amount = ''
    elif len(arr) == 1:
        if str(arr[0]).isdigit():
            pay_type = ''
            amount = str(arr[0])
        else:
            pay_type = str(arr[0])
            amount = ''
    elif len(arr) == 2:
        if str(arr[0]).isdigit():
            pay_type = str(arr[1])
            amount = str(arr[0])
        else:
            pay_type = str(arr[0])
            amount = str(arr[1])
    
    to_string = True
    ioae_buy = await infoOfAllExchanges(False, s1, s2, 'BUY', pay_type, amount)
    ioae_sell = await infoOfAllExchanges(False, s1, s2, 'SELL', pay_type, amount)
    #pprint(ioae_buy)
    spot = await prices(s1, s2)
    spot = spot[0]

    stability_list = {}
    # add vars in list from spot currency
    for i in spot:
        for i2 in i:
            if i.get(i2) != 0:
                stability_list[str(i2).replace(' ', '')] = [i.get(i2), True]
            else:
                stability_list[str(i2).replace(' ', '')] = [i.get(i2), False]


    for i in ioae_buy:
        if ioae_buy.get(i) == False:
            stability_list[str(f'{i}(p2p)#buy')] = [0, False]
        else:
            first_order = ioae_buy.get(i)[0]
            price = float(first_order[0])
            amount = float(first_order[1])
            minAmount = float(first_order[2])
            maxAmount = float(first_order[3])
            payMethods = first_order[4]
            
            stability_list[str(f'{i}(p2p)#buy')] = [price, amount, minAmount, maxAmount, payMethods, 1]
        #if ioae_buy.get(i) == False:
        #    print('False:', i)
        #pprint(i)

    for i in ioae_sell:
        if ioae_sell.get(i) == False:
            stability_list[str(f'{i}(p2p)#sell')] = [0, False]
        else:
            first_order = ioae_sell.get(i)[0]
            price = float(first_order[0])
            amount = float(first_order[1])
            minAmount = float(first_order[2])
            maxAmount = float(first_order[3])
            payMethods = first_order[4]
            
            stability_list[str(f'{i}(p2p)#sell')] = [price, amount, minAmount, maxAmount, payMethods, 2]
        #if ioae_buy.get(i) == False:
        #    print('False:', i)
        #pprint(i)

    result_dict = {}
    s_l = stability_list
    #print('s_l:\n')
    #pprint(s_l)
    st = list(sorted(s_l.items(), key=lambda x: x[1][0]))
    st.reverse()
    #print('st:\n')
    #pprint(st)

    buy_list = []
    sell_list = []
    for i in st:
        if str(i[1][-1]) == 'True' or i[1][-1] == 1:
            #print(1, i)
            buy_list.append(i)
        if str(i[1][-1]) == 'True' or i[1][-1] == 2:
            #print(2, i)
            sell_list.append(i)
        result_dict[i[0]] = float(i[1][0])

    rpc = ''
    if len(buy_list) == 0 or len(sell_list) == 0:
        rpc = False
    else:
        buy_price = min(buy_list, key=lambda x: x[1][0])
        sell_price = max(sell_list, key=lambda x: x[1][0])

        rpc = round((sell_price[1][0]/buy_price[1][0])*100 - 100, 3)
        #print(rpc)



    if to_string == True:
        result = f'📊{s1.upper()}/{s2.upper()}\n'
        for i in result_dict:
            if float(result_dict.get(i)) != 0:
                result += f'• {str(i).capitalize()}: <b>{result_dict.get(i)}</b>\n'
            else:
                result += f'• {str(i).capitalize()}: немає пари❄️\n'
        if rpc != False:
            result += f'\n🔥Найбільший спред: <b>{rpc}%</b>\n👉Купуємо на <b>{str(buy_price[0]).capitalize()}</b> по <b>{buy_price[1][0]}</b>\n👈Продаємо на <b>{str(sell_price[0]).capitalize()}</b> по <b>{sell_price[1][0]}</b>'
        else:
            result += '\n💢Не можемо порахувати спред😞'
    return result

    print('\n')
    pprint(buy_list)
    pprint(sell_list)
    print('\n', buy_price, sell_price, '\n')




#print(allP2Pprices(to_string, s1, s2, pay_type, amount))
#pprint(stability_list)

#pprint(ioae_buy)



































currency_list = {
    'Binance': [35.26, True],
    'Huobi': [38.63, True],
    # 1 - buy order, 2 - sell order
    'Binance(p2p)': [36.5, 1],
    
    'Huobi(p2p)': [38.69, 2],
    
    }

status_list = {
    'Binance': True,
    'Huobi': True,
    'Binance(p2p)': 'buy',
    'Huobi(p2p)': 'sell',
    }

def stringEr(currency_list, status_list):
    st = list(sorted(currency_list.items(), key=lambda x: x[1][0]))
    #print('lister ---- \n\n\n\n', lister)

    buy_list = []
    sell_list = []
    for i in st:
        if str(i[1][1]) == 'True' or str(i[1][1]) == '1':
            buy_list.append(i)
        elif str(i[1][1]) == 'True' or str(i[1][1]) == '2':
            sell_list.append(i)
    lister = min(buy_list, key=lambda x: x[1][0])
    
    print(lister, buy_list)

#stringEr(currency_list, status_list)






