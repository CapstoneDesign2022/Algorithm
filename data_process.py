from copy import deepcopy
import csv
import math, numpy
import datetime
import matplotlib.pyplot as plt


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
timestamp=[]

daystamp = 0 #날짜 구분을 위한 변수
day=0
dollor = []

#달러환율 저장
for i in USDT:
    dollor.append(float(i[4]))

for line in data:
    timestamp.append(float(line[0]))
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
    now = int(timestamp[i])/1000
    _date = datetime.datetime.fromtimestamp(int(now)).strftime('%Y-%m-%day %H:%M:%S')
    wr.writerow([timestamp[i+term-1], _date, premium[i+term-1], premium_av[i],upper_band[i],lower_band[i]])

f.close()

print(len(premium[term-1:]),len(premium_av),len(timestamp))


plt.plot(timestamp[term-1:],premium[term-1:],'r-',timestamp[term-1:],premium_av,'b-',timestamp[term-1:],upper_band,'g-',timestamp[term-1:],lower_band,'g-')
plt.show()