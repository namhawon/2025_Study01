''' 25 - 03 - 01 강의 자료 '''
import copy

'''
파이썬에서 문자열은 작은따옴표나 큰따옴표로 감싸서 표현을 한다.
'hi' , "hi"

주석 : 코드실행 결과에 영향을 미치지 않는 코드, 설명글

    1. 한 줄 주석 : # 을 써서 쓰는 한 줄 설명글
    2. 장문 주석 : 따옴표 ''' '''로 감싸서 문단을 바꿔가면서 길게 쓰는 설명글

실행 : 파이참에서는 첫째 줄 코드부터 작성된 모든 코드를 한 번에 실행시킨다.
        그래서 중간에 잘못 작성 된 코드가 있다면 실행을 멈춘다.

실행 단축키 : Shift + F10
주석 단축키 : Ctrl + ?
'''
# -------------------------------------------------------------------------------------------------------

''' 
변수(variable)
- 다양한 값을 지닌 하나의 속성
- 데이터 분석의 대상
- 파이썬에서 변수 지정은 등호(=)로 한다.
'''

apple = 1
# print(apple)
b = 2
c = 3
d = 3.5
# print(b)

### 변수 연산
# print(apple + b)
# print(apple + b + c)
# print(4 / d)

### 여러값으로 구성된 변수 생성 - list 사용 : 리스트는 [] 로 감싸지는 다중형 자료형
var1 = [1, 2, 3]
# print(var1[1]) # 인덱싱 - 특정 값만 리스트에서 뽑아 올 때

var2 = [4,5,6]
# print(var2)

# print(var1 + var2) # 리스트의 더하기 연산은 리스트를 합쳐준다.

### 문자로 된 변수 생성
str1 = 'a'
# print(str1)

str2 = 'text'
str3 = 'Hello World!'
# print(str2,str3) # print 문 안에서 ,(콤마) 와 함께 문자열을 나열하면 문자열이 한 줄에 나온다.

str4 = ['a','b','c',1,'1']
# print(str4)

str5 = ['Hello!','World','is','good!']
# print(str5)

# 파이썬에서는 공백을 인정을 한다.
# print(str2+' '+str3)

# 문자로 된 변수로는 숫자 연산을 할 수 없다.
# print(str2 + 2)

# ---------------------------------------------------------------------------------------------------
''' 함수(Function) 
- 값을 넣으면 특정한 기능을 수행해 처음과 다른 값을 반환하는 수
- 입력을 받아서 출력을 내는 수
'''

### 간단한 함수 사용
x = [1,2,3]

# print(sum(x)) # 함수는 괄호안에 입력을 받아서 사용한다.
# print(max(x))

### 함수의 결과를 변수로 지정해서 확인
x_sum_happy = sum(x)
# print(x_sum_happy)

# -----------------------------------------------------------------------------------------------------
''' 패키지(Package) 
- 함수가 여러 개 들어 있는 꾸러미
- 함수를 사용하려면 패키지 설치가 선행이 되어야한다.
- 아나콘다에 주요 패키지들이 대부분 들어있다.

패키지 설치하기 -> 패키지 로드 -> 패키지 함수 사용
'''

import matplotlib.pyplot as plt
'''
파이썬에서는 패키지 import 구문이 길어지거나 패키지명이 긴 경우에는 줄임말을 쓸 수 있다.
import 패키지명 as 별명
'''
import seaborn as sns

### 패키지 함수 사용
var = ['a','a','a','b','c','d','f','f']
# print(var)

# sns.countplot(x = var)
# plt.show()

### seaborn 의 titanic 데이터로 그래프 생성
# load_dataset() 로 데이터 로드

d = sns.load_dataset('titanic')
# print(d)

# sns.countplot(data = d, x='sex')
# plt.show()

# sns.countplot(data=d, x='class')
# plt.show()

### 함수의 추가 기능 사용 - x축 class, alive 별 색 표현
# sns.countplot(data=d, x='sex', hue='alive')
# plt.show()

## y축 class, alive 별 색표현 - 그래프 눕히기
# sns.countplot(data=d, y='class', hue='alive')
# plt.show()

# -----------------------------------------------------------------------------------------------------
''' 모듈(Module) : .py로 끝나는 파일 - 함수나 변수나 또는 클래스를 모아 놓은 파이썬 파일이다. '''

# '패키지명.모듈명.함수명()' 으로 함수 사용
import sklearn.metrics
# sklearn.metrics.accuracy_score()

# '모듈명.함수명()' 으로 사용 - from 절 사용 : from 패키지명 import 함수명
from sklearn import metrics
# metrics.accuracy_score()

# '함수명()' 으로 사용 - 단일 함수만 사용을 할 때
from sklearn.metrics import accuracy_score
# accuracy_score()

### 패키지 설치법
'''
1. 현재 아나콘다 환경에 존재하는 패키지 확인
왼쪽 하단 터미널 - 아나콘다 환경으로 접속 command prompt - conda list

2. 현재 환경에 패키지 설치법
왼쪽 하단 터미널 - 아나콘다 환경으로 접속 command prompt - pip install 패키지명


'''
import pydataset
a = pydataset.data()
# print(a)

# 패키지 함수를 사용
mt = pydataset.data('mtcars')
# print(mt)

# -------------------------------------------------------------------------------------------------------------
''' 데이터 프레임 (Data Frame)
- 데이터를 다룰 때 가장 많이 사용되는 데이터 형태 
- 구조가 엑셀과 비슷하다.
- 행과 열로 구성된 사각형 모양의 표처럼 생김


1. '열'은 속성이다. -> 컬럼(column) 또는 변수(variable)로 불림
2. '행'은 하나의 정보다. -> 로우(row) 또는 케이스(case)로 불림

데이터가 크다 = 행 또는 열이 많다.
'''

import pandas as pd

df = pd.DataFrame({'name':['김지훈','이유진','박동현','김민지'],
                   'english' : [90,80,60,70],
                   'math':[50,60,100,20]})
# print(df)

### 데이터 프레임 안의 값으로 분석

# 특정 변수를 추출
a = df['english']
# print(a)

# 변수의 값으로 합계
b = sum(a)
# print(b)

# 변수의 값으로 평균 구하기
# print('평균 :',b / 4)

# ----------------------------------------------------------------------------------------------------
''' 외부데이터 활용 '''

### 엑셀 파일 로드
path = 'C:/bigdata/PData/' # 내가 사용할 데이터들 모아 놓은 폴더 경로

df_exam = pd.read_excel(path +'excel_exam.xlsx')
# print(df_exam)

### 영어 평균
eng_mean = sum(df_exam['english']) / 20
# print('영어 평균 :',eng_mean)

### 길이 함수 len() 활용 - 괄호안에 들어오는 값의 길이를 반환하는 함수
x = [1,2,3,4,5,6]
# print(len(x))

m_mean = sum(df_exam['math']) / len(df_exam)
# print(m_mean)
# print(len(df_exam))

### 엑셀 파일의 첫 번째 행이 변수명이 아닌 경우
df_exam_novar = pd.read_excel(path + 'excel_exam_novar.xlsx',
                              header=None)
# print(df_exam_novar)

### 엑셀 파일에 시트가 여러 개 있다면?

# 1. Sheet2 시트 데이터 불러오기
# df_exam = pd.read_excel(path + 'excel_exam.xlsx', sheet_name='Sheet2')

# 2. 세 번째 시트 데이터 불러오기
# df_exam_3  = pd.read_excel(path + 'excel_exam.xlsx', sheet_name=2) # 숫자를 0부터 센다는 점 유의

### CSV 파일 로드
''' csv 파일 : 데이터 값을 쉼표와 줄바꿈으로 구분해놓은 파일 
- 용량이 비교적 작기 때문에 데이터를 주고 받는데 유용하다.
'''

csv = pd.read_csv(path + 'exam.csv')
# print(csv)

### 데이터 프레임을 csv 파일로 저장

df_mid = pd.DataFrame({
    'english' : [90,80,60,70],
    'math' : [50,60,100,20],
    'class' : [1,1,2,2]
})
# print(df_mid)
# df_mid.to_csv(path + 'output.csv')
# df_mid.to_csv(path + 'output.csv', index=False) # 인덱스를 저장하지 않을 때

# ----------------------------------------------------------------------------------------------------
''' 데이터 파악 - 확인 과정'''
'''
- 데이터 파악 함수들
1. head() : 앞 부분 출력
2. tail() : 뒷 부분
3. shape : 행, 열 개수 출력
4. info() : 변수 속성 출력
5. describe() : 요약 통계량 출력
'''

### 데이터 로드
exam = pd.read_csv(path + 'exam.csv')

### head()
# print(exam.head()) # 앞 행부터 5개 행까지 출력
# print(exam.head(10)) # 앞 행부터 10개 행까지 출력

### tail()
# print(exam.tail()) # 뒤 행부터 5개 행까지 출력
# print(exam.tail(9)) # 뒤 행부터 9개

### shape
# print(exam.shape) # 행과 열

### info()
# print(exam.info())
'''
변수 속성들
1. int64 : 정수
2. float64 : 실수
3. object : 문자
4. datetime64 : 날짜 시간 형식

64 - 64비트
    1. 1비트로 두 개의 값을 표현 가능
    2. int64 : 2^64개의 정수 표현 가능
'''

### describe() - 요약 통계량
# print(exam.describe())
''' std(표준편차) : 변수 안에 있는 값들이 평균에서 떨어진 정도를 나타낸 값 '''

### mpg 데이터 : R 에 ggplot2 라는 패키지의 예제 데이터 ( 미국 자동차 데이터 ) 파악
mpg = pd.read_csv(path + 'mpg.csv')
# print(mpg)
# print(mpg.info())
# print(mpg.describe(include='all'))
'''
unique : 고유값 빈도 - 중복을 제외한 범주의 개수
top : 최빈값 - 개수가 가장 많은 값
freq : 최빈값 빈도 - 개수가 가장 많은 값의 개수
'''

'''
- 함수들의 차이 

sum()                   pd.read_csv()                   df.head()
내장 함수               패키지 함수                     메서드 : 변수가 가지고 있는 함수

- 어트리뷰트 : 변수가 지니고 있는 값

df.shape
'''

### 변수명 수정

df = pd.DataFrame({'var1' : [1,2,1],
                   'var2' : [23,23,2]})
# print(df)

### 수정 전에 복사본 생성
'''
- 오류가 발생하더라도 원 상태로 복구가 가능하다
- 데이터를 원본과 비교하면서 변화 과정 확인 가능
'''
df_copy = df.copy() # 복사
# print(df_copy)

df_copy = df_copy.rename(columns = {'var2' : 'v2'}) # var2 를 v2 로 수정
# print(df_copy)
# print(df)

''' 
얕은 복사 : 원본과 복사본이 같은 객체를 참조한다.
'''
# org_list = [1, [2,3], 4]
#
# cop_list = copy.copy(org_list) # 얕은 복사
#
# # 원본과 복사본 출력
# print('원본 :', org_list)
# print('복사본 :', cop_list)
#
# # 원본 리스트 요소를 변경
# org_list[1][0] = 'A'
#
# # 변경 후 출력
# print('변경 후 원본 :', org_list)
# print('변경 후 복사본 :', cop_list)

### 파생변수 : 기존에 존재하는 변수를 사용해서 새로 만드는 변수

# 1. 변수 조합을 사용해서 파생변수 생성
# 1. mpg 데이터 통합 연비 변수 생성
# print(mpg)

mpg['total'] = (mpg['cty'] + mpg['hwy'])/2
# print(mpg.head())

total_mean = sum(mpg['total'])/len(mpg)
# print('미국 자동차들의 평균 통합 연비 :',total_mean )

# 2. 조건문을 활용해 파생변수 생성 - 합격 판정 변수 생성
# 2-1. 합격 기준 정하기
mean = mpg['total'].describe()
# print(mean)

# 2-2. 합격 판정 변수 만들기 (기준 : 20)
import numpy as np

mpg['test'] = np.where(mpg['total'] >= 20, 'PASS','FAIL')
# print(mpg.head(25))

# 2-3. 빈도표로 합격 판정 자동차 수 살펴보기
a = mpg['test'].value_counts() # 빈도표 생성 함수
# print(a)

# 2-4. 막대 그래프로 빈도 표현
count_test = mpg['test'].value_counts()
# count_test.plot.bar(rot=0) # 빈도 그래프 확인용
# plt.show()

### 중첩 조건문 활용 - 조건문 안의 조건문 : 자동차의 등급을 매기기
'''
A : 통합연비가 30이상
B : 20 ~ 29
C : 20미만
'''

# 연비 등급 변수 만들기
mpg['grade'] = np.where(mpg['total']>=30, 'A Grade',
                        np.where(mpg['total']>=20, 'B Grade', 'C Grade'))
# print(mpg.head(25))

# 빈도표 생성 후 막대로 등급 살펴보기
count_grade = mpg['grade'].value_counts()
# print(count_grade)

# count_grade.plot.bar(rot=0)
# plt.show()

# 알파벳 순으로 막대 정렬
count_grade = mpg['grade'].value_counts().sort_index() # 알파벳순 정렬 추가
# print(count_grade)
# count_grade.plot.bar(rot=0)
# plt.show()

### 목록에 해당하는 변수 생성
'''
| : 버티컬 바
- 또는(or) 을 의미하는 기호
- shift + ￦ 로 입력
'''
# small 차와 large 차로 구분해주는 파생변수 size 생성
# -> compact , subcompact, 2seater 를 small 로 구분 그 외는 모두 large
mpg['size'] = np.where((mpg['category'] == 'compact')|
                       (mpg['category'] == 'subcompact')|
                       (mpg['category'] == '2seater'), 'SMALL', 'LARGE')
a = mpg['size'].value_counts()
# print(a)

# df.isin() 활용
mpg['size'] = np.where(mpg['category'].isin(['compact','subcompact','2seater']),
                       'small','large')
b = mpg['size'].value_counts()
# print(b)

''' midwest.csv 는 미국 동북중부 400여개 지역의 인구통계 정보를 담고있는 데이터다.
    
Q1. midwest.csv 를 불러오고 데이터를 파악하시오.

Q2. poptotal (전체 인구) 변수를 total 로, popasian(아시아인 인구 수) 변수를 asian로 수정하세요.   
    
Q3. total, asian 변수를 사용해서 전체 인구대비 아시아 인구 백분율 파생변수를 추가하세요.     
    '''

# Q1.
midwest = pd.read_csv(path + 'midwest.csv')
# print(midwest.info())
# print(midwest.describe())

# Q2.
midwest = midwest.rename(columns={'poptotal':'total'})
midwest = midwest.rename(columns={'popasian':'asian'})
print(midwest.head())

# Q3.
# 백분율 변수 먼저 추가
midwest['ratio'] = midwest['asian']/midwest['total'] * 100

# 히스토그램으로 표현
midwest['ratio'].plot.hist()
plt.show()