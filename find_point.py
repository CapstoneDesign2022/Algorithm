def deal_high_premium(binance_seed,binance_coin,up_seed,up_coin,binance_avg,up_avg): #김프가 높을때 업비트 매도 바이낸수 매수
    binance_seed=binance_seed-binance_avg
    binance_coin=binance_coin+1
    up_seed=up_seed+up_avg
    up_coin=up_coin-1

    return binance_seed,binance_coin,up_seed,up_coin
## 사고팔때 발생하는 수수료 계산해놓기

def deal_zero_premium(binance_seed,binance_coin,up_seed,up_coin,binance_avg,up_avg): #김프이동평균선과 김프가 만날때
    if(up_coin>binance_coin): #업코인이 더 많으면 L to H
        binance_seed=binance_seed-binance_avg
        binance_coin=binance_coin+1
        up_seed=up_seed+up_avg
        up_coin=up_coin-1
    elif(up_coin<binance_coin): #업이 적으면
        binance_seed=binance_seed+binance_avg
        binance_coin=binance_coin-1
        up_seed=up_seed-up_avg
        up_coin=up_coin+1

    return binance_seed,binance_coin,up_seed,up_coin

def deal_low_premium(binance_seed,binance_coin,up_seed,up_coin,binance_avg,up_avg): #김프가 낮을 때 업비트 매수 바이낸수 매도
    binance_seed=binance_seed+binance_avg
    binance_coin=binance_coin-1
    up_seed=up_seed-up_avg
    up_coin=up_coin+1

    return binance_seed,binance_coin,up_seed,up_coin