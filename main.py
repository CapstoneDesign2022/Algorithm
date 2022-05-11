import matplotlib.pyplot as plt
from find_point import *
from data_process import *

binanceSeed = 500000 #달러
binanceCoin = 10
upSeed = 1000000000 #원화
upCoin = 10

# 임의의 기준 값 조절 # zero는 default
pos_point_value = 0.015
neg_point_value = -0.02
zero_point_value = 0.00

# 고점, 변곡점(-), 저점, 변곡점(+)
high_point = 0
p_to_n_point = 0 # positive to negative
low_point = 0
n_to_p_point = 0 # negative to positive


for i in range(n_to_p_point, len(sub)-1):
    if sub[i] >= pos_point_value:
        high_point = i
        cnt = i
        #tmp1.append(high_point)
        print(f"point is {i}")
        break

for i in range(high_point, len(sub)-1):
    if sub[i] > zero_point_value and sub[i+1] < zero_point_value:
        p_to_n_point = i
        cnt = i
        #tmp2.append(p_to_n_point)
        print(f"point is {i}")
        break

for i in range(p_to_n_point, len(sub)-1):
    if sub[i+1] <= neg_point_value:
        low_point = i
        cnt = i
        #tmp3.append(low_point)
        print(f"point is {i}")
        break

for i in range(low_point, len(sub)-1):
    if sub[i] < zero_point_value and sub[i+1] > zero_point_value:
        n_to_p_point = i
        cnt = i
        #tmp4.append(n_to_p_point)
        print(f"point is {i}")
        break

print("while is end!")

plt.plot(sub,'r-')

plt.axhline(y=pos_point_value)
plt.axhline(y=neg_point_value)
plt.axhline(y=zero_point_value)

plt.scatter(x=high_point, y=sub[high_point], c="black", marker=".", zorder=3)
plt.scatter(x=p_to_n_point, y=sub[p_to_n_point], c="black", marker=".", zorder=3)
plt.scatter(x=low_point, y=sub[low_point], c="black", marker=".", zorder=3)
plt.scatter(x=n_to_p_point, y=sub[n_to_p_point], c="black", marker=".", zorder=3)

# plt.scatter(x=tmp1, y=[sub[i] for i in tmp1], c="black", marker=".", zorder=3)
# plt.scatter(x=tmp2, y=[sub[i] for i in tmp2], c="black", marker=".", zorder=3)
# plt.scatter(x=tmp3, y=[sub[i] for i in tmp3], c="black", marker=".", zorder=3)
# plt.scatter(x=tmp4, y=[sub[i] for i in tmp4], c="black", marker=".", zorder=3)




open_up, close_up = 0, 0
close_bn, close_bn = 0, 0

import pandas as pd
data = pd.read_csv('plus.csv')
df = pd.DataFrame(data)
#print(df.iloc[point, 1])

# 원하는 point 선택
# high_point / p_to_n_point / low_point / n_to_p_point
point = high_point

real_point = point + term

def findUBT(df, point):
    open = df.iloc[point, 1]
    close = df.iloc[point, 4]

    return (open + close) / 2

def findBNC(df, point):
    open = df.iloc[point, 7]
    close = df.iloc[point, 10]

    return (open + close) / 2


up_avg = findUBT(df, real_point)
bn_avg = findBNC(df, real_point)

D = [27755,29121,40104,43987]

startb,startu = binanceSeed,upSeed
up_avg = findUBT(df,D[0])
bn_avg = findBNC(df,D[0])
binanceSeed,binanceCoin,upSeed,upCoin = deal_high_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)
# print(binanceSeed,binanceCoin,upSeed,upCoin)

up_avg = findUBT(df,D[1])
bn_avg = findBNC(df,D[1])
binanceSeed,binanceCoin,upSeed,upCoin = deal_zero_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)

up_avg = findUBT(df,D[2])
bn_avg = findBNC(df,D[2])
binanceSeed,binanceCoin,upSeed,upCoin = deal_low_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)

up_avg = findUBT(df,D[3])
bn_avg = findBNC(df,D[3])
binanceSeed,binanceCoin,upSeed,upCoin = deal_zero_premium(binanceSeed,binanceCoin,upSeed,upCoin,bn_avg,up_avg)


print("시작 : ",startb,startu)
print(binanceSeed,binanceCoin,upSeed,upCoin)
print("끝 : ",binanceSeed,upSeed,"원")
# print("이득 : ", binanceSeed*dollor+upSeed - start,"원")
plt.show() 
# print(f"open_UBT = {open_up}, close_UBT = {close_up} \nopen_BNC = {open_bn}, close_BNC = {close_bn}")