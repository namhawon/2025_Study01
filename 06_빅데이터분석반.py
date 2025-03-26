''' 25 - 03 - 15 강의 자료 '''
import matplotlib.pyplot as plt

''' 한국복지패널데이터 분석

- 한국보건사회연구원 발간 조사 자료
- 전국 7천여 가구 선정, 매년 추적 조사한 자료
- 경제활동, 생활실태, 복지욕구 등 천여개 변수로 구성이 됨.
- 다양한 분야의 연구자, 정책전문가들이 활용
'''
### 패키지 설치
'comand prompt -> pip install pyreadstat'

### 사용할 패키지
import pandas as pd
import numpy as np
import seaborn as sns

### 데이터 로드
path = 'C:/bigdata/PData/'

raw_welfare = pd.read_spss(path + 'Koweps_hpwc14_2019_beta2.sav')

# 1. 복사본 생성
welfare = raw_welfare.copy()

### 데이터 검토
# print(welfare)
# print(welfare.info())

# 1. 자주 사용할 변수명 수정
welfare = welfare.rename(columns = {'h14_g3' : 's', # 성별
                                    'h14_g4' : 'birth', # 태어난 연도
                                    'h14_g10' : 'marriage_type', # 혼인 상태
                                    'h14_g11' : 'religion', # 종교
                                    'p1402_8aq1' : 'income', # 월급
                                    'h14_eco9' : 'code_job', # 직업 코드
                                    'h14_reg7' : 'code_region'}) # 지역 코드

'''
분석 절차
1단계 - 변수 검토 및 전처리
    -> 변수의 특징 파악, 이상치와 결측치 정제
    -> 변수의 값을 우리가 다루기 쉽게 바꾸기
    -> 분석할 변수 각각 전처리
2단계 - 변수간 관계 분석
    -> 데이터 요약 표, 그래프 생성
    -> 분석 결과 해석 -> 시각화
'''

''' 성별에 따른 월급 차이 -  성별에 따라 월급이 다를까 ? '''

### 성별 변수 검토 및 전처리
a = welfare['s'].dtypes
# print(a)

# 빈도 확인
a = welfare['s'].value_counts()
# print(a)

# 결측치 확인
a = welfare['s'].isna().sum()
# print('결측치 개수 :', a)

# 성별 항목 이름 부여
welfare['s'] = np.where(welfare['s'] == 1, 'male', 'female')
a = welfare['s'].value_counts()
# print(a)

# 성별 빈도 막대 생성
# sns.countplot(data=welfare, x='s')
# plt.show()

### 월급 변수 검토 및 전처리

# 검토
a = welfare['income'].dtypes
# print(a)

# print(welfare['income'].describe()) # 요약 통계량

# 히스토그램
# sns.histplot(data=welfare, x='income')
# plt.show()

# 결측치 확인
# a = welfare['income'].isna().sum()
# print(a)

### 성별에 따른 월급 차이 분석
s_income = welfare.dropna(subset='income') \
    .groupby('s', as_index=False) \
    .agg(mean_income = ('income', 'mean'))
# print(s_income)

# 시각화
# sns.barplot(data=s_income, x='s', y='mean_income')
# plt.show()

''' 나이와 월급의 관계 - 우리나라 사람은 몇 살에 가장 돈을 많이 버는가 ? '''
# print(welfare['birth'].dtypes)

# print(welfare['birth'].describe())
# sns.histplot(data=welfare, x='birth')
# plt.show()

# 이상치 확인
# print(welfare['birth'].describe())
welfare['birth'] = np.where(welfare['birth'] > 2014, np.nan, welfare['birth'])

# 결측치 확인
a = welfare['birth'].isna().sum()
# print(a)

# 파생변수 - 나이
welfare = welfare.assign(age = 2019 - welfare['birth'] + 1)
a = welfare['age'].describe()
# print(a)
# sns.histplot(data=welfare, x='age')
# plt.show()

### 나이와 월급의 관계 분석
# 1. 나이에 따른 월급 평균표
age_income = welfare.dropna(subset=['age', 'income'])\
    .groupby('age')\
    .agg(mean_income=('income','mean'))
# print(age_income.head(10))

# 2. 그래프
# sns.lineplot(data=age_income, x='age',y='mean_income')
# plt.show()

''' 연령대에 따른 월급 차이 
 
 - 기준
 young : 30미만
 middle : 30~59
 old : 60 이상
'''
# 연령대 변수 생성
welfare = welfare.assign(ageg = np.where(welfare['age'] < 30, 'young',
                                         np.where(welfare['age'] <= 59,'middle','old')))
# 빈도 구하기
a = welfare['ageg'].value_counts()
# print(a)

# 빈도 막대 그래프
# sns.countplot(data=welfare, x='ageg')
# plt.show()

### 연령대에 따른 월급 차이 분석

# 1. 연령대에 따른 월급 평균표 생성
ageg_income = welfare.dropna(subset = 'income') \
    .groupby('ageg', as_index=False) \
    .agg(mean_income = ('income', 'mean'))
# print(ageg_income)

# 2. 막대 그래프
# sns.barplot(data=ageg_income, x='ageg', y='mean_income')
# plt.show()

# 3. 막대 정렬
# sns.barplot(data=ageg_income, x='ageg', y='mean_income',
#             order=['young','middle','old'])
# plt.show()

''' 연령대 및 성별 월급 차이 분석 '''
# 1. 연령대 및 성별 월급 평균표 생성
s_income = welfare.dropna(subset = 'income')\
    .groupby(['ageg','s'], as_index=False)\
    .agg(mean_income = ('income','mean'))
# print(s_income)

# 2. 막대그래프
# sns.barplot(data=s_income, x='ageg', y='mean_income', hue='s',
#             order=['young','middle','old'])
# plt.show()

''' 직업별 월급 차이 - 어떤 직업이 돈을 가장 많이 버는가 ? '''

### 직업 변수 검토 및 전처리

# print(welfare['code_job'].dtypes)
# a = welfare['code_job'].value_counts()
# print(a)

#  코드북의 직종코드 시트 읽어오기
list_job = pd.read_excel(path + 'Koweps_Codebook_2019.xlsx', sheet_name = '직종코드')
# print(list_job.head())
# print(list_job.shape)

# welfare 에 list_job 결합 - 매칭
welfare = welfare.merge(list_job, how = 'left', on = 'code_job')

# code_job 결측치 제거하고 code_job, job 출력
b = welfare.dropna(subset = ['code_job'])[['code_job','job']].head
# print(b)

### 직업별 월급 차이 분석
# 1. 직업별 월급 평균표
job_income = welfare.dropna(subset=['job','income'])\
    .groupby('job', as_index=False)\
    .agg(mean_income = ('income','mean'))
# print(job_income.head())

# 2. 시각화 - 월급이 많은 직업 상위 10개
top10 = job_income.sort_values('mean_income', ascending=False).head(10)
# print(top10)

# 3. 한글 폰트 설정
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family' : 'Malgun Gothic'})

# 4. 그래프 출력
# sns.barplot(data=top10, x='mean_income', y='job')
# plt.show()

''' 지역별 연령대 비율 - 어느 지역에 노인 인구가 많을까 ? '''

### 지역 변수 검토 및 전처리
a = welfare['code_region'].dtypes
# print(a)

b = welfare['code_region'].value_counts()
# print(b)

# 1. 지역 코드 목록 만들기
list_region = pd.DataFrame({'code_region' : [1,2,3,4,5,6,7],
                            'region' : ['서울',
                                        '수도권(인천/경기)',
                                        '부산/울산/경남',
                                        '대구/경북',
                                        '대전/충남',
                                        '강원/충북',
                                        '광주/전남/전북/제주도']})
# print(list_region)

# 2. 지역명 변수를 데이터에 추가
welfare = welfare.merge(list_region, how='left', on='code_region')
# print(welfare[['code_region', 'region']].head(25))

### 지역별 연령대 비율 분석
region_ageg = welfare.groupby('region',as_index = False)\
    ['ageg']\
    .value_counts(normalize=True)
# print(region_ageg)

# 1. 시각화
region_ageg = region_ageg.assign(proportion  = region_ageg['proportion']*100) \
    .round(1) # 반올림
# print(region_ageg)

# sns.barplot(data=region_ageg, y='region', x='proportion', hue='ageg')
# plt.show()

# 2. 누적 비율 막대 그래프
''' 피벗 : 사용자가 설정한 레이아웃으로 자료를 재배치하는 것 '''
# 피벗
pivot_df = region_ageg[['region','ageg','proportion']].pivot(index = 'region',
                                                             columns = 'ageg',
                                                             values = 'proportion')
# print(pivot_df)
# 가로 막대 그래프
# pivot_df.plot.barh(stacked=True)
# plt.show()

# 막대 정렬
reor_df = pivot_df.sort_values('old')[['young','middle','old']]
# print(reor_df)

# 누적 가로 막대 그래프
# reor_df.plot.barh(stacked = True)
# plt.show()
# ---------------------------------------------------------------------------------------------------------------

''' 통계적 분석 기법 활용한 가설 검정 

1. 기술통계 : 데이터를 요약해서 설명하는 통계 분석 기법
2. 추론통계 : 어떤 값이 발생할 확률을 계산하는 통계 분석 기법

ex) 성별에 따른 월급 차이가 우연히 발생할 확률을 계산
    - 이런 차이가 우연히 나타날 확률이 작다면
        -> 성별에 따른 월급 차이가 통계적으로 유의하다. 고 결론
    - 이런 차이가 우연히 나타날 확률이 크다면
        -> 성별에 따른 월급 차이가 통계적으로 유의하지 않다. 고 결론

※ 기술 통계 분석에서 집단 간 차이가 있는 것으로 나타났더라도 이는 우연에 의한 차이일 수 있다.
-> 신뢰할 수 있는 결론을 내리려면 유의확률을 계산하는 통계적 가설 검정 절차를 거쳐야함.

3. 통계적 가설 검정 : 유의확률을 이용해서 가설을 검정하는 방법
4. 유의확률(p-value) : 실제로는 집단 간 차이가 없는데, 우연히 차이가 있는 데이터가 추출될 확률

    - 유의확률이 크면
        -> 집단 간 차이가 통계적으로 유의하지 않다. 고 해석
    - 유의확률이 작다면
        -> 집단 간 차이가 통계적으로 유의하다. 고 해석
'''

''' t - 검정 (t-test) : 두 집단의 평균에 통계적으로 유의한 차이가 있는지 알아볼 때 사용하는 통계 분석 기법 '''
mpg = pd.read_csv(path + 'mpg.csv')

### 기술 통계 분석 - compact 차와 suv 차의 도시 연비 차이
a = mpg.query('category in ["compact", "suv"]') \
    .groupby('category', as_index=False) \
    .agg(car_count = ('category', 'count'),
         mean = ('cty', 'mean'))
# print(a)
'''
비교하는 집단의 분산(값이 퍼져 있는 정도)이 같은지 여부에 따라 적용하는 공식이 다름
equal_var = True : 집단 간 분산이 같다고 가정
'''
compact = mpg.query('category == "compact"')['cty'] # 컴팩트 자동차 행만 추출하고 그의 도심 연비 열만 추출
suv = mpg.query('category == "suv"')['cty']

# t-test
from scipy import stats
t = stats.ttest_ind(compact, suv, equal_var=True)
# print(t)
'''
일반으로 유의확률 5%를 판단의 기준으로 삼는다.
- p-value 가 0.05 미만이면 집단 간 차이가 통계적으로 유의하다고 해석 

TtestResult(statistic=np.float64(11.917282584324107), pvalue=np.float64(2.3909550904711282e-21), df=np.float64(107.0))

해석 :
- 실체로는 차이가 없는데 이런 정도의 차이가 우연히 관찰될 확률이 5% 보다 작다면,
    이 차이를 우연이라고 보기 어렵다고 결론
    2.3909550904711282e-21 : 2.3909550904711282 x 10의 -21승 -> 지수표현식
    
- p-value가 0.05 보다 작기 때문에 "compact와 suv 간 평균 도시 연비 차이가 통계적으로 유의하다." 고 결론
'''

### fl 변수 , 일반 휘발유(r) 와 고급 휘발유(p)의 도시 연비 t 검정
regular = mpg.query('fl == "r"')['cty']
premium = mpg.query('fl == "p"')['cty']

# t-test
t = stats.ttest_ind(regular, premium, equal_var=True)
# print(t)
'''
pvalue=np.float64(0.28752051088667036)

해석 : 
p-value 가 0.05보다 큼.
실제로는 차이가 없는데 우연에 의해 이정도의 차이가 관찰될 확률 28.75%

일반 휘발유와 고급 휘발를 사용하는 자동차의 도시 연비 차이가 통계적으로 유의하지 않다.
'''

''' 상관분석 : 두 연속 변수가 서로 관련이 있는지 검정하는 통계 분석 기법 

- 상관계수 
    - 두 변수가 얼마나 관련되어 있는지, 관련성 정도를 파악할 수 있다.
    - 0~1 사이의 값, 1에 가까울수록 관련성이 크다는 의미
    - 양수면 정비례, 음수면 반비례 관게
'''

### 실업자 수와 개인 소비 지출의 상관관계

# economics 로드
economics = pd.read_csv(path + 'economics.csv')

# 상관행렬 생성
c = economics[['unemploy','pce']].corr()
# print(c)

# 유의확률 구하기 - 상관분석
c = stats.pearsonr(economics['unemploy'], economics['pce'])
# print(c)
''' 유의확률이 0.05미만이므로 실업자 수와 개인 소비 지출간의 상관관계가 
    통계적으로 유의하다. '''

### 상관행렬 히트맵 생성
# - 모든 변수의 상관관계를 나타낼 때 사용

mtcars = pd.read_csv(path + 'mtcars.csv')
# print(mtcars.head())

# 1. 상관행렬 만들기
car_cor = mtcars.corr()
# print(car_cor)
car_cor = round(car_cor, 2) # 소수점 둘째 자리까지 반올림
# print(car_cor)

# 2. 히트맵 생성 : 값의 크기를 색 진하기로 표현
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.dpi' : '120',
                     'figure.figsize' : [7.5, 5.5]}) # 가로 세로 크기 설정

import seaborn as sns
# sns.heatmap(car_cor,
#             annot = True, # 상관계수 표시 여부
#             cmap = 'RdBu')
# plt.show()

# 3. 대각행렬 제거 : 히트맵은 대각선 기준으로 왼쪽 아래와 오른쪽 위의 값이 대칭해서 중복됨. -> mask 로 제거

# 3-1. mask 생성 : 상관행렬의 행과 열의 수 만큼 0으로 채운 배열(array)을 만듬
import numpy as np
mask = np.zeros_like(car_cor)
# print(mask)

# 3-2. 오른쪽 위 대각 행렬을 1로 바꾸기
mask[np.triu_indices_from(mask)] = 1
# print(mask)

# 3-3. 히트맵에 적용
# sns.heatmap(car_cor,
#             annot=True,
#             cmap='RdBu',
#             mask= mask)
# plt.show()

# 3-4. 빈 행과 열 제거 : mask의 첫 번째 행과 마지막 열을 제거해서 빈 행과 열 제거
mask_new = mask[1:, :-1]
cor_new = car_cor.iloc[1:, :-1] # 상관행렬의 첫 번째 행, 마지막 열 제거

# sns.heatmap(cor_new,
#             annot = True,
#             cmap= 'RdBu',
#             mask=mask_new)
# plt.show()

# 4. 보기좋게 수정하는 여러 옵션
# sns.heatmap(cor_new,
#             annot = True,
#             cmap= 'RdBu',
#             mask=mask_new,
#             linewidths=.5, # 경계 구분선 추가
#             vmax = 1, # 가장 진한 파란색으로 표현할 최대값
#             vmin = -1, # 가장 진한 빨간색으로 표현할 최소값
#             cbar_kws={'shrink':.5}) # 범례 크기를 줄이기
# plt.show()

# --------------------------------------------------------------------------------------------------------------
''' 텍스트 마이닝 : 문자로 된 데이터에서 유의미한 정보를 캐내는 작업 
    - 문장을 구성하는 어절들의 품사를 분석
    - 텍스트 마이닝할 때 가장 먼저 하는 작업
    - 명사, 동사, 형용사 등 의미를 지닌 품사를 추출해서 빈도를 확인
'''
'''
1. 내 컴퓨터 운영체제에 맞는 자바 설치 
2. 시스템 환경 변수 편집 - 환경변수 - 시스템 환경변수 JAVA_HOME, path 세팅
3. KoNLPy의 의존성 패키지 설치 - pip install jpype1
4. KoNLPy를 설치
5. 테스팅 오류 발생할 시 - 시스템 환경 변수 편집 - 환경변수 - 사용자 변수에 JAVA_HOME 추가 - server 폴더 경로 삽입 
'''
import konlpy
# hannanum = konlpy.tag.Hannanum()
# h = hannanum.nouns('ㄷ안녕하세요 빅데이터 분석 강의중 입니다. 반갑습니다.')
# print(h)

### 연설문 로드
'''
파이썬에서 텍스트 파일을 읽어올 때 open() 함수를 쓰게 된다.

인코딩 : 컴퓨터가 문자를 표현하는 방식, 문서마다 인코딩 방식이 다르기 때문에 문서 파일과 프로그램의
        인코딩이 맞지 않으면 문자가 깨진다.

인코딩 : 어떠한 정보를 특수한 목적을 가지고 다른 형태로 변환하는 행위 
디코딩 : 인코딩된 데이터를 원래의 형태로 되돌리는 행위
'''

moon = open(path + 'speech_moon.txt', encoding='UTF-8').read()
# print(moon)

### 가장 많이 사용한 단어를 확인 - 당시 대통령의 정서 확인
import re # 문자 처리 패키지
'''
정규표현식 : 특정한 규칙을 가진 문자열을 표현하는 단어식
[^가-힣] : 한글이 아닌 모든 문자라는 뜻을 가진 정규표현식
'''
moon = re.sub('[^가-힣]',' ',moon)
# print(moon)

# 2. 명사 추출 - nouns() 사용
hannanum = konlpy.tag.Hannanum()

nouns = hannanum.nouns(moon)
# print(nouns)

# 3. 데이터 프레임으로 변환
import pandas as pd

df_word = pd.DataFrame({'word':nouns})
# print(df_word)

# 4. 단어 길이 변수 추가
df_word['word_len'] = df_word['word'].str.len()
# print(df_word.head(30))

# 4-1. 두 글자 이상 단어만 남기기
df_word = df_word.query('word_len >= 2')
# print(df_word.sort_values('word_len'))

# 4-2. 단어 빈도 생성
df_word = df_word.groupby('word', as_index=False)\
    .agg(n = ('word','count'))\
    .sort_values('n', ascending=False)
# print(df_word)

# 5. 단어 빈도 막대 그래프
top20 = df_word.head(20)

import matplotlib.pyplot as plt
import seaborn as sns

# sns.barplot(data=top20, x='n', y='word')
# plt.show()

### 워드 클라우드 생성 : 단어 구름 시각화

# 패키지 설치 - pip install wordcloud

# 한글 폰트 설정
font = 'C:/Windows/Fonts/HMKMMAG.TTF' # 폰트 선정 후 경로 지정

# 단어와 빈도를 담은 딕셔너리를 생성 - 워드클라우드는 입력을 딕셔너리 형태로 받게 되어있다.
dic_word = df_word.set_index('word').to_dict()['n'] # 데이터 프레임을 딕셔너리 형태로 변환
# print(dic_word)

# 생성
from wordcloud import WordCloud
# wc = WordCloud(
#     random_state=1234, # 난수 고정
#     font_path=font, # 폰트 설정
#     width=400, # 가로 크기
#     height=400, # 세로 크기
#     background_color='white' # 배경색
# )
# img_wordcloud = wc.generate_from_frequencies(dic_word) # 워드클라우드 생성
# plt.figure(figsize=(10,10)) # 가로세로 크기설정
# plt.axis('off') # 테두리선 없애기
# plt.imshow(img_wordcloud) # 출력물을 지정
# plt.show() # 출력

# 5. 워드클라우드 모양 바꾸기

# 5-1. mask 만들기
import PIL # 이미지 처리 패키지

icon = PIL.Image.open(path + 'cloud.png')

import numpy as np

img = PIL.Image.new('RGB', icon.size, (255,255,255))
img.paste(icon, icon)
img = np.array(img)
# print(img)

# 5-2 워드클라우드에 mask 적용
wc = WordCloud(
    random_state=1234, # 난수 고정
    font_path=font, # 폰트 설정
    width=400, # 가로 크기
    height=400, # 세로 크기
    mask=img, # 마스크 이미지 삽입
    colormap='inferno', # 글자 컬러맵
    background_color='white' # 배경색
)
img_wordcloud = wc.generate_from_frequencies(dic_word) # 워드클라우드 생성
plt.figure(figsize=(10,10)) # 가로세로 크기설정
plt.axis('off') # 테두리선 없애기
plt.imshow(img_wordcloud) # 출력물을 지정
plt.show() # 출력


