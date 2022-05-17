# import datetime
# now = '1442154124'
# _date = datetime.datetime.fromtimestamp(int(now)).strftime('%Y-%m-%d %H:%M:%S')

# print(_date)

# 용어	설명
# 평균(mean, average)	주어진 변량(데이터)를 모두 합하여, 전체 개수로 나눈 값(산술평균임을 가정)
# 편차(deviation)	변량에서 평균을 뺀 값

# 분산(Varance)	편차의 제곱의 평균, 편차의 경우 음수와 양수를 가질 수 있는데 그냥 더해서 사용하면 상쇄가 되므로,
#  양수로 맞추기 위해 제곱을 수행합니다. 분산의 의미는 평균으로부터 변량이 얼마나 떨어져 있는지(퍼져 있는지) 나타냅니다.

# 표준편차(Standard deviation)	분산에 루트를 씌운 값, 
# 양수로 만들기 위해 제곱을 수행한 분산을 원래의 스케일로 돌리기 위해서 제곱근을 구한 값을 사용합니다.
from copy import deepcopy
import math
a= [1,2,3,4,5,6]

print(a[0:2])

mean = 0
for i in a:
    mean+=i
mean = mean/len(a)
print(mean)

b=[]
for i in a:
    b.append(i-mean)
print(b)

sd = 0
for i in b:
    sd+=i*i
sd=sd/len(b)
print(math.sqrt(sd))

c=deepcopy(a)
print(a)
d=a
a.append(7)
print(a)
print(d)
print(c)
import numpy

std = numpy.std(c)
print(std)