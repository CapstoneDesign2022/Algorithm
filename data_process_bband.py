from copy import deepcopy
import csv
import math, numpy
import dateterm
import matplotlib.pyplot as plt
import pandas as pd

from find_point import *


f = open('plus.csv','r',encoding= 'utf-8')
data = csv.reader(f)

f = open('USDT.csv','r',encoding = 'utf -8')
USDT = csv.reader(f)


#김치 프리미엄 구하기
#김프 = 업비트 가격 / (바낸가격 * 달러환율)

# 김프 구하기
term = 10000 #김프평균을 구할 때 n기간을 나타냄
premium = [] #매분시간의 김프
premium_av=[] #김프 n기간만큼의 평균
termstamp=[]

daystamp = 0 #날짜 구분을 위한 변수
day=0
dollor = []

#달러환율 저장
for i in USDT:
    dollor.append(float(i[4]))

for line in data:
    termstamp.append(float(line[0]))
    Up = (float(line[1])+float(line[4]))/2 #업비트 시가 종가의 평균 (시가+종가/2)
    Bi = (float(line[7])+float(line[10]))/2 #바낸 시가 종가의 평균 (시가+종가/2)

    if (daystamp ==0):
        daystamp = float(line[0])
    else:
        if(float(line[0]) - daystamp <86400000):
            day=day
        elif(float(line[0]) - daystamp == 86400000):
            daystamp = float(line[0])
            day+=1

    premium.append( Up / Bi / dollor[day])


std=[] #표준편차

#김프 평균 구하기
sum,s,e=0,0,0
for i in range(len(premium)-1):

        if(e-s < term):
            sum = sum + premium[e]
            e+=1
            if(e-s==term):
                premium_av.append(sum/term)
                std.append(numpy.std(premium[s:e]))
        if(e-s == term):
            sum = sum-premium[s]+premium[e]
            premium_av.append(sum/term)
            std.append(numpy.std(premium[s:e]))
            s+=1
            e+=1

upper_band=[] #   20일 김프 이평선 값 + ( 20일 동안의 김프 표준편차 값 ) * 2
lower_band=[] #   20일 김프 이평선 값 - ( 20일 동안의 김프 표준편차 값 ) * 2

for i in range(len(std)):
    upper_band.append(premium_av[i]+(std[i]*2))
    lower_band.append(premium_av[i]-(std[i]*2))


#현재 김프와 김프 평균의 차이
sub = []
for i in range(len(premium)-term+1):
    sub.append(premium[i+term-1]-premium_av[i])

f=open('data.csv','w',newline='')
wr=csv.writer(f)
for i in range(len(premium_av)):
    now = int(termstamp[i])/1000
    _date = dateterm.dateterm.fromtermstamp(int(now)).strfterm('%Y-%m-%day %H:%M:%S')
    wr.writerow([termstamp[i+term-1], _date, premium[i+term-1], premium_av[i],upper_band[i],lower_band[i]])

f.close()

print(len(premium[term-1:]),len(premium_av),len(termstamp))


# plt.plot(termstamp[term-1:],premium[term-1:],'r-',termstamp[term-1:],premium_av,'b-',termstamp[term-1:],upper_band,'g-',termstamp[term-1:],lower_band,'g-')
# plt.show()

high_meet = []
low_meet = []
#zero_meet = []

def find_highest(start):
    highest = term-1

    for i in range(start, len(upper_band)-1):
        now = premium[term-1+i]
        next = premium[term+i]

        if now >= lower_band[i] and next <= lower_band[i+1]:

            cut = i

            return highest, cut


        if now <= upper_band[i] and next >= upper_band[i+1]:
            point = term+i
            if highest == term-1:
                highest = point
            else:
                if premium[point] >= premium[highest]:
                    highest = point

    return -1, -1

def find_lowest(start):
    lowest = term-1

    for i in range(start, len(upper_band)-1):
        now = premium [term-1+i]
        next = premium [term+i]

        if now <= upper_band[i] and next >= upper_band[i+1]:

            cut = i

            return lowest, cut


        if now >= lower_band[i] and next <= lower_band[i+1]:
            point = term+i
            if lowest == term-1:
                lowest = point
            else:
                if premium[point] <= premium[lowest]:
                    lowest = point
    
    return -1, -1


# find_zero 함수 => 다른 함수와 연결시 결과가 이상해서 수정 필요
"""
def find_zero(start_h2l, start_l2h):
    if start_h2l != 0 : # high to low
        for i in range(start_h2l, len(upper_band)-1):
            now_t = term-1+i
            next_t = now_t + 1

            if premium[now_t] >= premium_av[now_t] and premium[next_t] <= premium_av[next_t]:
                zero_point = now_t
                cut = i
                return zero_point, cut

        return -1, -1
            

    elif start_l2h != 0 : # low to high
        for i in range(start_l2h, len(upper_band)-1):
            now_t = term-1+i
            next_t = now_t + 1

            if premium[now_t] <= premium_av[now_t] and premium[next_t] >= premium_av[next_t]:
                zero_point = now_t
                cut = i
                return zero_point, cut

        return -1, -1

"""

highest_, swap_p2n = find_highest(0)
lowest_, swap_n2p = find_lowest(0)



if highest_ == term-1:
    start_point = swap_n2p
    low_meet.append(lowest_)

    highest = term-1
    lowest = term-1

    while 1:
        # zero_point, mid_n2p = find_zero(0, start_point)

        # if zero_point == -1 :
        #     break
        # else:
        #     start_point = mid_n2p
        #     zero_meet.append(zero_point)

        highest, swap_p2n = find_highest(start_point)

        if highest == -1 :
            break
        else:
            start_point = swap_p2n
            high_meet.append(highest)
        
        #print(f"highest = {highest}")

        # zero_point , mid_p2n = find_zero(start_point, 0)

        # if zero_point == -1 :
        #     break
        # else:
        #     start_point = mid_p2n
        #     zero_meet.append(zero_point)

        lowest, swap_n2p = find_lowest(start_point)

        if lowest == -1 :
            break
        else:
            start_point = swap_n2p
            low_meet.append(lowest)

        #print(f"lowest = {lowest}")

elif lowest_ == term-1:
    start_point = swap_p2n
    high_meet.append(highest_)

    highest = term-1
    lowest = term-1

    while 1:
        # zero_point , mid_p2n = find_zero(start_point, 0)

        # if zero_point == -1 :
        #     break
        # else:
        #     start_point = mid_p2n
        #     zero_meet.append(zero_point)

        lowest, swap_n2p = find_lowest(start_point)

        if lowest == -1 :
            break
        else:
            start_point = swap_n2p
            low_meet.append(lowest)

        # zero_point, mid_n2p = find_zero(0, start_point)

        # if zero_point == -1 :
        #     break
        # else:
        #     start_point = mid_n2p
        #     zero_meet.append(zero_point)

        highest, swap_p2n = find_highest(start_point)

        if highest == -1 :
            break
        else:
            start_point = swap_p2n
            high_meet.append(highest)
        

plt.plot(termstamp[term-1:], premium[term-1:],'r-',
         termstamp[term-1:],premium_av,'b-',
         termstamp[term-1:],upper_band,'g-',
         termstamp[term-1:],lower_band,'g-')

plt.scatter(x=[termstamp[i] for i in high_meet], y=[premium[i] for i in high_meet], c="black", marker=".", zorder=3)
plt.scatter(x=[termstamp[i] for i in low_meet], y=[premium[i] for i in low_meet], c="black", marker=".", zorder=3)
#plt.scatter(x=[termstamp[i] for i in zero_meet], y=[premium[i] for i in zero_meet], c="black", marker=".", zorder=3)



binanceSeed = 500000 #달러
binanceCoin = 10
upSeed = 1000000000 #원화
upCoin = 10

deal_points = high_meet + low_meet
deal_points = sorted(deal_points)

data = pd.read_csv('plus.csv')
df = pd.DataFrame(data)

def findUBT(df, point):
    open = df.iloc[point, 1]
    close = df.iloc[point, 4]

    return (open + close) / 2

def findBNC(df, point):
    open = df.iloc[point, 7]
    close = df.iloc[point, 10]

    return (open + close) / 2

    flag = 0

if deal_points[0] == high_meet[0]: #at the highest
    flag = 1

elif deal_points[0] == low_meet[0]: # at the lowest
    flag = 2




startb,startu = binanceSeed,upSeed


for deal_point in deal_points:
    
    up_avg = findUBT(df, deal_point)
    bn_avg = findBNC(df, deal_point)
    
    if flag == 1:
        binanceSeed,binanceCoin,upSeed,upCoin = deal_high_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)
        flag = 2
    elif flag == 2:
        binanceSeed,binanceCoin,upSeed,upCoin = deal_low_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)
        flag = 1
        

print("시작 : ",startb,startu)
print(binanceSeed,binanceCoin,upSeed,upCoin)
print("끝 : ",binanceSeed,upSeed,"원")
#print("이득 : ", (binanceSeed-startb)*dollor+upSeed - startu,"원")

plt.show() 