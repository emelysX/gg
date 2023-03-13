from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
from talib.abstract import *
import pandas as pd
import numpy as np
import time
import talib

#LOGIN E SENHA
my_user = "emelybeatriz695@gmail.com"
my_pass = "wali1234"

#CONFIGURAÇÃO SE ESTÁ LOGADO OU NÃO
Iq=IQ_Option(my_user,my_pass)
iqch1,iqch2=Iq.connect()
if iqch1==True:
  print("logado ( ͡ ° ͜ʖ ͡ °)")
else:
  print("login failed ┌( ಠ_ಠ)-💣")
  
#BANCA TOTAL
my_blc=Iq.get_balance()
print(f"BANCA TOTAL: {my_blc} ")

#QUER O MODO PRATICO OU REAL
changeB = input("Pratica ou Real? 1- Pratica 2- Real:") 
if changeB == '1':
    changeBs = 'PRACTICE'
elif changeB == '2':
    changeBs = 'REAL'

# Vai usar dinheiro FICTICIO OU REAL = PRACTICE / REAL
Iq.change_balance(changeBs) 

#ESCOLHA O VALOR DE ENTRADA
valorPR = input("Escolha o valor de entrada :")



#ESCOLHA QUAL MOEDA
def BinDig(): 
    OptionBD = "1"
    global par 
    if OptionBD == '1': 
        OptionBx = input("Escolha a opção Digital: 1-USD/CAD 2-EUR/USD 3-AUD/CAD 4-AUD/JPY 5-EUR/AUD 6-EUR/GBP 7-GBP/USD 8-GBP/JPY 9-EUR/USD-OTC 10-EUR/JPY-OTC 11-AUD/CAD-OTC: ")
        if OptionBx == '1':
            parX = 'USDCAD'
        elif OptionBx == '2':
            parX = 'EURUSD'
        elif OptionBx == '3':
            parX = 'AUDCAD'
        elif OptionBx == '4':
            parX = 'AUDJPY'
        elif OptionBx == '5':
            parX = 'EURAUD'
        elif OptionBx == '6':
            parX = 'EURGBP'
        elif OptionBx == '7':
            parX = 'GBPUSD' 
        elif OptionBx == '8':
            parX = 'GBPJPY' 
        elif OptionBx == '9':
            parX = 'EURUSD-OTC'
        elif OptionBx == '10':
            parX = 'EURJPY-OTC' 
        elif OptionBx == '11':
            parX = 'AUDCAD-OTC'
        
        par = parX
        print('Voce selecinou a opção:'+OptionBx+'-'+par)
        print('...Aguarde.')
BinDig()

total_ganho = 0

def apostarDescerD():
    duration=5#minute 1 or 5
    amount=valorPR
    action="put"#call
    stop_loss = 2.00
    
    global total_ganho

    Iq.subscribe_strike_list(par,duration)
    _,id=Iq.buy_digital_spot(par,amount,action,duration)
    print(id)
    print("__DIGITAL APOSTOU DESCER__")
    while True:
        PL=Iq.get_digital_spot_profit_after_sale(id)
        if PL!=None:
            time.sleep(1)
        print("valor: ", PL, end='\r')
        if PL > 0.10 * int(valorPR):
            Iq.close_digital_option(id)
            print("ganho")
            total_ganho += PL
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
            break
        elif PL < -stop_loss:
            Iq.close_digital_option(id)
            print("perda")
            total_ganho += PL
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
            break

def apostarSubirD():
    duration=5#minute 1 or 5
    amount=valorPR
    action="call"#put
    stop_loss = 2.00
    
    global total_ganho

    Iq.subscribe_strike_list(par,duration)
    _,id=Iq.buy_digital_spot(par,amount,action,duration)
    print(id)
    print("__DIGITAL APOSTOU SUBIR__")
    while True:
        PL=Iq.get_digital_spot_profit_after_sale(id)
        if PL!=None:
            time.sleep(1)
        print("valor: ", PL, end='\r')
        if PL > 0.10 * int(valorPR):
            Iq.close_digital_option(id)
            print("ganho")
            total_ganho += PL
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
            break
        elif PL < -stop_loss :
            Iq.close_digital_option(id)
            print("perda")
            total_ganho += PL
            print("Ganho atual: R$", total_ganho)
            time.sleep(10)
            break
        
size = 60 #periodo da vela
timeperiod = 9 #periodo do rsi

print("Starting stream...")
Iq.start_candles_stream(par, size, maxdict=60)

while True:
    candles = Iq.get_realtime_candles(par, size)
    inputs = {
        'close': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'volume': np.array([])
    }
    for timestamp, candle in candles.items():
        inputs["close"] = np.append(inputs["close"], candle["close"])
        inputs["high"] = np.append(inputs["high"], candle["max"])
        inputs["low"] = np.append(inputs["low"], candle["min"])
        inputs["volume"] = np.append(inputs["volume"], candle["volume"])

    rsi = talib.RSI(inputs["close"], timeperiod=timeperiod)
    mfi = talib.MFI(inputs["high"], inputs["low"], inputs["close"], inputs["volume"], timeperiod=7)
    print("MFI", mfi[-1] ,"RSI:", rsi[-1], end='\r')
    


    if mfi[-1] > 70:
        apostarDescerD()
    elif mfi[-1] < 30:
        apostarSubirD()

    #ema = talib.EMA(inputs["close"], timeperiod=20)
    #mfi = talib.MFI(inputs["high"], inputs["low"], inputs["close"], inputs["volume"], timeperiod=7)
    #stoch = talib.STOCH(inputs["high"], inputs["low"], inputs["close"], fastk_period=timeperiod, slowk_period=timeperiod, slowd_period=timeperiod)
    #k = stoch[0][-1]
    #d = stoch[1][-1]

