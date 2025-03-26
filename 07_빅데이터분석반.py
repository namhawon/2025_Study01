''' 25 - 03 - 08 강의 자료 '''
from string import printable
from traceback import print_tb

import matplotlib.pyplot as plt
from pandas import read_csv

''' Review -

'''
# ---------------------------------------------------------------------------------------------------
''' 
데이터 가공 - 데이터 분석 전처리 
: 분석에 적합하게 데이터를 가공하는 작업
: Pandas 패키지 

- 데이터 가공 함수
1. query(조건) : 조건에 맞는 데이터 추출 (행)
2. 데이터명[] : 필요한 변수 추출 (열) 
3. sort_values() : 순서대로 정렬 / ascending = False -> 내림차순
4. assign() : 파생변수 추가
5. groupby() : 집단화
6. agg() : 요약통계량 
7. merge() : 가로로 합치기 , 매칭
8. concat() : 세로로 합치기
'''
### 조건에 맞는 데이터 추출 - 행 추출 : query()

# 데이터 로드
path = 'C:/bigdata/PData/'

import pandas as pd
exam = pd.read_csv(path + 'exam.csv')
# print(exam)

# 반이 1반인 경우만 추출
a = exam.query('nclass == 1') # query 함수 안의 조건은 따옴표로 감싸준다.
# print(a)

# 반이 1반이 아닌 경우만 추출
a = exam.query('nclass != 1')
# print(a)

## 초과, 미만, 이상, 이하 조건 걸기

# 1. 수학 점수가 50점을 초과한 학생만 추출
a = exam.query('math > 50')
# print(a)

# 2. 영어 점수가 50점 이상인 경우
a = exam.query('english >= 50')
# print(a)

## 여러가지 조건을 충족하는 행 추출

# 1. 1반이면서 수학점수가 50점 이상인 경우
a = exam.query('nclass == 1 & math >= 50')
# print(a)

## 여러 조건 중 하나 이상 충족하는 행 추출

# 1. 수학 점수가 90점 이상이거나 영어 점수가 90점 이상인 경우
a = exam.query('math >= 90 | english >= 90') # | : 버티컬 바 - or 의 의미를 가지는 기호
# print(a)

## 목록에 해당하는 행 추출

# 1반, 3반, 5반에 해당하면 추출
a = exam.query('nclass == 1 | nclass == 3 | nclass == 5')
# print(a)

b = exam.query('nclass in [1,3,5]')
# print(b)

### 문자 변수를 사용해서 조건에 맞는 행 추출
# -> '전체 조건'과 '추출할 문자'에 서로 다른 따옴표를 입력
df = pd.DataFrame({'s' : ['F','M','F','M'],
                   'country' : ['Korea','USA','China','Japan']})
# print(df)

a = df.query('s == "F" & country == "Korea"')
# print(a)

# 별도의 외부 변수를 사용해서 행을 추출하려면 변수명 앞에 @를 붙여서 조건 입력
var = 3
a = exam.query('nclass == @var')
# print(a)

### 필요한 변수 추출 - df['변수명']
# print(exam['math'])

# 1. 여러 변수 추출
# print(exam[['nclass','math','english']])
''' 대괄호를 두 번 쓰면 데이터 프레임으로 추출이 되고,
    한 번 쓰면 시리즈로 추출이 된다. '''

# 2. 변수 제거
a = exam.drop(columns = 'math')
# print(a)

b = exam.drop(columns = ['math', 'english'])
# print(b)
# print(exam)

### query() 와 [] 조합하기

# 1. 수학 점수가 50점 이상인 학생의 id 와 math 만 추출
a = exam.query('math >= 50')[['id','math']]
# print(a)

# 2. 가독성있게 코드 줄 바꿈하기
b = exam.query('math >= 50') \
    [['id','math']] \
    .head()
# print(b)

### 순서대로 정렬 - df.sort_values()
a = exam.sort_values('math') # 수학 점수 오름차순 정렬
# print(a)

# 내림차순
a = exam.sort_values('math', ascending=False) # 내림차순 정렬
# print(a)

# 1. 정렬 기준을 여러가지로 적용

# nclass, math 오름차순 정렬
a = exam.sort_values(['nclass','math'])
# print(a)

# nclass 오름차순, math 내림차순 정렬
a = exam.sort_values(['nclass','math'], ascending=[True, False])
# print(a)

'''
Q . mpg 데이터를 읽어와서 'audi' 에서 생산한 자동차 중에 어떤 자동차 모델의 hwy(고속도로 연비)가 높은지
    알아보려한다. 'audi'에서 생산한 자동차 중 hwy가 1~7위에 해당하는 자동차의 데이터를 출력하시오.
'''
mpg = pd.read_csv(path + 'mpg.csv')

result = mpg.query('manufacturer == "audi"')\
    [['model','hwy']]\
    .sort_values('hwy', ascending=False)\
    .head(7)
# print(result)

### 파생변수 추가 - df.assign()

# 총점 변수 추가
a = exam.assign(total = exam['math'] + exam['english'] + exam['science'])
# print(a)
# print('-'*100)
# print(exam)

# 여러가지 파생변수 한 번에 추가
a = exam.assign(total = exam['math'] + exam['english'] + exam['science'],
                mean = (exam['math'] + exam['english'] + exam['science']) / 3)
# print(a)

# assign에 np.where 적용 - 조건문 적용
import numpy as np
a = exam.assign(test = np.where(exam['science'] >= 60, 'pass', 'fail'))
# print(a)

# 추가한 변수를 pandas 함수에 바로 적용
a = exam.assign(total = exam['math'] + exam['english'] + exam['science']) \
    .sort_values('total')
# print(a)

### 집단별로 요약하기 - groupby(), agg()

# 1. 전체 요약 통계량 구하기 - math 평균 구하기
a = exam.agg(mean_math = ('math', 'mean'))
# print(a)

# 2. 집단별로 요약
a = exam.groupby('nclass') \
    .agg(mean_math = ('math','mean'))
# print(a)

# 3. 변수를 인덱스로 바꾸지 않기 - as_index = False
''' 인덱스(Index) : 값이 데이터 상에 어디에 있는지 "값의 위치를 나타낸 값" '''
b = exam.groupby('nclass', as_index=False) \
    .agg(mean_math = ('math','mean'))
# print('-'*100)
# print(b)

# 4. 여러가지 요약통계량 한 번에 출력하기
c = exam.groupby('nclass') \
    .agg(mean_math = ('math','mean'),
         sum_math = ('math','sum'),
         median_math = ('math','median'),
         n = ('nclass','count'))
# print(c)

''' agg() 에 자주 사용하는 요약통계량 함수
1. mean() : 평균
2. std() : 표준편차
3. sum() : 합계
4. median() : 중앙값
5. min() : 최소값
6. max() : 최대값
7. count() : 빈도 (개수)
'''
# 5. 집단별로 다시 집단 나누기 - mpg 데이터 제조사별 구동방식별 차량 분리
# print(mpg)

a = mpg.groupby(['manufacturer', 'drv']) \
    .agg(mean_cty = ('cty','mean'))
# print(a)

'''
Q . 제조 회사별로 "suv" 자동차의 도시 및 고속도로 합산 연비 평균을 구해서 내림차순으로 정렬하고
    1~5등까지 출력하기.
'''
# print(mpg.head(20))
a = mpg.query('category == "suv"') \
    .assign(total = (mpg['cty'] + mpg['hwy'])/2) \
    .groupby('manufacturer') \
    .agg(mean_total = ('total', 'mean')) \
    .sort_values('mean_total', ascending = False) \
    .head(5)
# print(a)

### 데이터 합치기 - df.merge() , df.concat()

# 1. 가로로 합치기
test1 = pd.DataFrame({'id':[1,2,3,4,5],
                      'mid' : [60,80,70,90,85]})
test2 = pd.DataFrame({'id':[1,2,3,4,5],
                      'fin' : [70,83,65,95,80]})
# print(test1)
# print(test2)

'''
pd.merge() 에 결합할 데이터 프레임명 나열
how = 'left' : 오른쪽에 입력한 데이터 프레임을 왼쪽 프레임에 결합
on : 데이터를 합칠 때 기준으로 삼을 변수명 입력
'''

# id 기준으로 합쳐서 total 에 할당
total = pd.merge(test1, test2, how='left', on='id')
# print(total)

# 다른 데이터를 활용해서 변수 추가 - 매칭
name = pd.DataFrame({'nclass':[1,2,3,4,5],
                     'teacher':['KIM','JUNG','PARK','LEE','CHOI']})
# print(name)
# print(exam)

exam_n = pd.merge(exam, name, how='left', on='nclass')
# print(exam_n)

# 세로로 합치기
g_a = pd.DataFrame({'id' : [1,2,3,4,5],
                    'test' : [60,80,70,90,85]})
g_b = pd.DataFrame({'id' : [6,7,8,9,10],
                    'test': [70,83,65,95,100]})
# print(g_a)
# print(g_b)
''' 결합할 데이터 프레임 이름을 []를 사용해서 나열 '''
g_all = pd.concat([g_a, g_b])
# print(g_all)

# 인덱스 중복 x
g_all = pd.concat([g_a, g_b], ignore_index=True)
# print(g_all)

# -----------------------------------------------------------------------------------------------------------------
''' 데이터 정제 - 빠진 데이터, 이상한 데이터 찾기 

결측치(Missing Value) : 누락된 값, 비어 있는 값
- 데이터 수집 과정에서 발생할 오류로 포함될 가능성
- 함수가 적용되지 않거나 분석 결과가 왜곡되는 문제 발생
- 실제로 데이터 분석시 결측치 확인, 제거 후 분석
'''
### 결측치 찾기

import pandas as pd
import numpy as np

df = pd.DataFrame({'s' : ['M','F',np.nan,'M','F'],
                   'score' : [5,4,3,4,np.nan]})
# print(df)

# NaN 있는 상태로 연산
# print(df['score'] + 1) # 출력도 NaN

# 1. 결측치 확인
# print(pd.isna(df))
# print(pd.isna(df).sum())

# 2. 결측치 제거

# 2-1. 결측치가 있는 행을 제거
a = df.dropna(subset='score')
# print(a)

# 2-2. 여러 변수에 결측치 없는 데이터 추출
df_nomiss = df.dropna(subset=['s','score'])
# print(df_nomiss)

# 2-3. 결측치가 하나라도 있으면 제거
df_nomiss2 = df.dropna()
'''
df.dropna() 에 아무런 변수도 입력하지 않는다.
-> 모든 변수에 결측치가 없는 행만 남김

- 간편하긴 하지만 사용할 수 있는 데이터도 제거가 될 수 있다.
- 분석에 사용할 변수를 직접 지정해서 결측치 제거하는 방법을 권장
'''

# 3. 결측치 대체
'''
- 결측치가 적고 데이터가 크면 그냥 제거해도 무방하다.
- 데이터 작고, 결측치 많다면 데이터 손실이 커져서 분석 결과가 왜곡이 된다.
-> 결측치 대체법을 활용해서 보완

- 결측치 대체법 : 결측치를 제거하는 대신에 다른 값을 채워 넣는 방법
    -> 대표값(평균, 최빈값 등)을 구해서 일괄 대체
    -> 통계 분석 기법을 활용해서 예측값 추정 후 대체
'''
# print(exam)
exam.loc[[2,7,14], ['math']] = np.nan # 2, 7, 14행의 math 에 NaN 할당
# print(exam)

# 평균값 구하기
a = exam['math'].mean()
# print(a) # 55.235

# df.fillna() 로 결측치를 평균값으로 대체
exam['math'] = exam['math'].fillna(55)
# print(exam)

# 대체 후 확인
a = exam['math'].isna().sum()
# print(a)

''' 이상치(anomaly) : 정상 범위에서 크게 벗어난 값 '''

### 이상치 제거 - 존재할 수 없는 값
# -> 논리적으로 존재할 수 없는 값이 있을 경우 결측치로 변환 후 제거
    # ex) 성별 변수에 1(남), 2(여자) 외 3이나 9라는 값이 있다면 그 값을 NaN 변환

# 이상치 데이터 생성
df = pd.DataFrame({'s' : [1,2,1,3,2,1],
                  'score' : [5,4,3,4,2,6]})
# print(df)

# 이상치 확인 - 빈도표를 만들어 존재할 수 없는 값이 있는지 확인
a = df['s'].value_counts(sort=False).sort_index()
# print(a)

# 결측 처리 - 이상치일 경우 NaN 부여
df['s'] = np.where(df['s']==3, np.nan, df['s'])
# print(df)
df['score'] = np.where(df['score'] > 5, np.nan, df['score'])
# print(df)

# 결측 처리가 완료되면 결측치 제거 후 분석
a = df.dropna(subset=['s','score']) \
    .groupby('s') \
    .agg(mean_math = ('score','mean' ))
# print(a)

### 이상치 제거 - 극단적인 값
'''
극단치(outlier) : 논리적으로 존재할 수 있지만 극단적으로 크거나 작은 값
- 극단치가 존재하면 분석 결과 왜곡
- 기준 정하기
    1. 논리적 판단(ex. 성인 몸무게 40~150kg 벗어난다면 매우 드물기 때문에 극단치로 간주)
    2. 통계적 기준(ex. 상하위 0.3% 또는 +-3 표준편차 벗어나면 극단치로 간주)
    3. 상자 그림(boxplot)을 사용해서 중심에서 크게 벗어난 값을 극단치로 간주

- 상자 그림(box plot) : 데이터의 분포를 상자 모양으로 표현한 그래프
    1. 중심에서 멀리 떨어진 값을 점으로 표현
    2. 상자 그림을 이용해 극단치 기준 구할 수 있음
'''
### 상자 그림 살펴보기
# print(mpg)
import seaborn as sns
import matplotlib.pyplot as plt

# sns.boxplot(data=mpg, y='hwy')
# plt.show()
'''
상자 아래 세로선 : 아랫 수염 - 하위 0~25%에 해당하는 값
상자 밑면 : 1사분위수(Q1) - 하위 25% 위치 값
상자 내 굵은선 : 2사분위수(Q2) - 50% 위치 값 (중앙값)
상자 윗면 : 3사분위수(Q3) - 하위 75% 위치 값
상자 위 세로선 : 윗 수염 - 하위 75~100%에 해당하는 값
상자 밖 가로선 : 극단치 경계 - Q1, Q3 밖 1.5IQR 내 최대값
상자 밖 점 표식 : 극단치 - Q1, Q3 밖 1.5IQR을 벗어난 값

- IQR(사분위 범위) : 1사분위수와 3사분위수의 거리 - 3사분위수에서 1사분위수 뺀 값
- 1.5IQR : IQR의 1.5배
'''

# 1. 극단치 기준값 구하기

# 1-1. 1사분위수, 3사분위수 구하기
pct25 = mpg['hwy'].quantile(.25)
pct75 = mpg['hwy'].quantile(.75)
# print('1사분위수 :', pct25)
# print('3사분위수 :', pct75)

# 1-2. iqr 구하기
iqr = pct75 - pct25
# print('IQR :', iqr)

# 1-3. 하한, 상한 구하기
# print('하한 :', pct25 - 1.5 * iqr)
# print('상한 :', pct75 + 1.5 * iqr)

# 1-4. 극단치 결측 처리 - 4.5 ~ 40.5 를 벗어나면 NaN 부여
mpg['hwy'] = np.where((mpg['hwy'] < 4.5) | (mpg['hwy'] > 40.5), np.nan, mpg['hwy'])

# 1-5. 결측치 빈도 확인
a = mpg['hwy'].isna().sum()
# print(a)

# 2. 결측치 제외하고 분석
b = mpg.dropna(subset=['hwy']) \
    .groupby('drv')\
    .agg(mean_hwy = ('hwy','mean'))
# print(b)
# ------------------------------------------------------------------------------------------------------------
''' 파이썬 그래프 '''
'''
- 추세와 경향성이 드러나 데이터의 특징을 쉽게 이해하기 위해서 그래프를 사용
- 새로운 패턴을 발견, 데이터의 특징을 잘 전달
- 다양한 그래프
    1. 2차원 그래프, 3차원 그래프
    2. 지도 그래프
    3. 네트워크 그래프
    4. 모션차트
    5. 인터랙티브 그래프
    
- seaborn 패키지
    -> 그래프를 만들 때 자주 사용되는 패키지
    -> 코드가 쉽고 간결함
'''

### 산점도(Scatter Plot) : 데이터를 x축과 y축에 점으로 표현한 그래프
# -> 나이와 소득처럼 연속값으로 구성된 변수간의 관계를 표현할 때 자주 사용

import seaborn as sns
import pandas as pd
mpg = pd.read_csv(path + 'mpg.csv')

# x축에 displ(배기량), y축은 hwy(고속도로 연비)를 나타낸 산점도 만들기
# sns.scatterplot(data=mpg, x='displ', y='hwy')
# plt.show()

# 축 범위 설정

# x 축 범위 3 ~ 6 제한, y 축 범위 10~30 제한
# sns.scatterplot(data=mpg, x='displ', y='hwy') \
#     .set(xlim = [3,6], ylim = [10,30])
# plt.show()

# 종류별로 색깔 다르게 표현 - drv 별
# sns.scatterplot(data=mpg, x='displ', y='hwy', hue='drv')
# plt.show()

''' 그래프 설정 - 데이터 분석할 때 미리 세팅 '''
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi':'150', # 해상도 : 기본값 72
                     'figure.figsize':[8,6], # 그림 크기, 기본값 [6,4]
                     'font.size':'15', # 글자 크기, 기본값 10
                     'font.family':'Malgun Gothic'}) # 폰트, 기본값 sans-serif

# 모든 설정 되돌리기
# plt.rcParamsDefault()

### 막대 그래프(bar chart) : 데이터의 크기를 막대의 길이로 표현한 그래프
# -> 성별 소득 차이처럼 집단 간 차이를 표현할 때 사용

# 1. 평균막대그래프

# 1-1. 집단별 평균표 생성
df_mpg = mpg.groupby('drv', as_index=False) \
    .agg(mean_hwy = ('hwy','mean'))
# print(df_mpg)

# 1-2. 막대 생성
# sns.barplot(data=df_mpg, x='drv', y='mean_hwy')
# plt.show()

# 2. 크기순으로 막대 정렬하기
# 2-1. 데이터 프레임을 정렬
df_mpg = df_mpg.sort_values('mean_hwy', ascending=False)

# 2-2. 막대 그래프 생성
# sns.barplot(data=df_mpg, x='drv', y='mean_hwy')
# plt.show()

# 3. 빈도막대그래프 : 값의 빈도(개수)를 막대의 길이로 표현
# -> 여러 집단의 빈도 비교할 때 사용

# 3-1. 집단별 빈도표 생성
df_mpg = mpg.groupby('drv', as_index=False)\
    .agg(n = ('drv', 'count'))
# print(df_mpg)

# 3-2. 막대 그래프 생성
# sns.barplot(data=df_mpg, x='drv', y='n')
# plt.show()

# 3-3. sns.countplot() 으로 빈도막대그래프 만들기
# -> 집단별 빈도 그래프 만드는 작업을 생략하고 원자료를 사용해서 바로 만듦
# sns.countplot(data=mpg, x='drv')
# plt.show()

# 3-4. countplot() 막대 정렬 - 4, f, r 순으로
# sns.countplot(data=mpg, x='drv', order = ['4','f','r'])
# plt.show()

# 3-5. 빈도가 높은 순으로 정렬 - drv 값으로
a = mpg['drv'].value_counts().index
# print(a)

# sns.countplot(data=mpg, x='drv', order = a)
# plt.show()

# 4. 자동차 중에 어떤 category가 많은지 알아보려한다. sns.barplot()을 사용해서 자동차 종류별 빈도 막대 그래프
# -> 막대는 빈도가 높은순으로 정렬
df_mpg = mpg.groupby('category', as_index=False)\
    .agg(n = ('category', 'count'))\
    .sort_values('n', ascending=False)
# print(df_mpg)

# 4-1. 시각화 - 막대
# sns.barplot(data=df_mpg, x='category', y='n', hue='category')
# plt.show()

### 선 그래프(line chart) : 데이터를 선으로 표현한 그래프
# - 시간에 따라 달라지는 데이터를 표현할 때 사용 (환율, 주가지수,....)
# 시계열 데이터(time series data) : 일별 환율처럼, 일정 시간 간격을 두고 나열된 데이터
# 시계열 그래프(time series chart) : 시계열 데이터를 선으로 표현한 그래프

# 1. 시계열 그래프 생성 - economics 데이터
economics = pd.read_csv(path + 'economics.csv')
# print(economics.head())

# sns.lineplot(data=economics, x='date', y='unemploy')
# plt.show()

# 2. x 축에 연도만 표시하기

# 2-1. 날짜 시간 타입 변수 생성
economics['date2'] = pd.to_datetime(economics['date'])

# print(economics.info())

# print(economics[['date','date2']])

# 2-2. 연 추출
y = economics['date2'].dt.year
# print(y)

# 2-3. 월 추출
m = economics['date2'].dt.month
# print(m)

# 2-4. 일 추출
d = economics['date2'].dt.day
# print(d)

# 3. 연도 변수 만들기
economics['year'] = economics['date2'].dt.year
# print(economics.head())

# 4. x 축에 연도 표시
# sns.lineplot(data=economics, x='year', y='unemploy')
# plt.show()

# 5. 신뢰구간 제거
# sns.lineplot(data=economics, x='year', y='unemploy', errorbar=None)
# plt.show()

### 상자그림 (box plot) : 데이터 분포 또는 퍼져있는 형태를 직사각형 상자 모양으로 표현한 그래프
# -> 데이터가 어떻게 분포하고 있는지 알 수 있다.
# -> 평균값만 볼 때보다 데이터의 특징을 더 자세하게

# sns.boxplot(data = mpg, x='drv', y='hwy')
# plt.show()