''' 25 - 02 - 15 강의 자료 '''

''' Review -

mpg <- as.data.frame(ggplot2::mpg)

1. 데이터 파악
head() : 데이터 앞부분
tail() : 데이터 뒷부분
View() : 데이터 뷰어 창에서 확인
dim() : 데이터 차원
str() : 데이터 속성
summary() : 요약 통계량

2. 데이터 가공

exam %>% filter(english >= 90)
exam %>% filter(class == 1 & math >= 50) and
exam %>% filter(math >= 90 | english >= 90) or

exam %>% select(math)
exam %>% select(class, math, english)

exam %>% arrange(math) 오름차순
exam %>% arrange(desc(math)) 내림차순
exam %>% arrange(class, math)

exam %>% mutate(total = math + english + science,
                mean = (math + english + science)/3)
exam %>% mutate(test = ifelse(science >= 60, "pass", "fail"))          

exam %>% group_by(class) %>% summarise(mean_math = mean(math))

# 각 집단별로 다시 집단 나누기 - mpg 데이터에서 제조사 별로 구동 방식별 집단화
mpg %>% 
  group_by(manufacturer, drv) %>% 
  summarise(mean_cty = mean(cty))

total <- left_join(test1, test2, by="id") 가로로 합치기

group_all <- bind_rows(group_a, group_b) 세로로 합치기
'''

# ------------------------------------------------------------------------------
''' 데이터 정제 - 빠진 데이터, 이상한 데이터 제거 '''
'''
결측치(Missing Value)
- 누락된 값, 비어있는 값
- 함수 적용 불가, 분석 결과 왜곡
- 제거 후 분석 실시
'''

### 결측치 찾기

df <- data.frame(s = c('M','F', NA, 'M','F'),
                 score = c(5,4,3,4,NA))
df

# 결측치 확인
is.na(df)

# 결측치 빈도 확인
table(is.na(df))

# 변수별로 결측치 확인
table(is.na(df$s))

# 결측치  포함된 상태로 분석
mean(df$score)
sum(df$score)

### 결측치 제거
# 결측치가 있는 행 제거
library(dplyr)

df %>% filter(is.na(score)) # score에서 NA 인 데이터만 출력

new_df <- df %>% filter(!is.na(score)) # score 에서 결측치가 아닌 데이터만 출력 - 제거

# 결측치 제외한 데이터로 분석
df_nomiss <- df %>% filter(!is.na(score))
df_nomiss
mean(df_nomiss$score)
sum(df_nomiss$score)

# 여러 변수 동시에 결측치 없는 데이터 추출
df_nomiss <- df %>% filter(!is.na(s) & !is.na(score))
df_nomiss

# 결측치가 하나라도 존재하면 제거
df_nomiss2 <- na.omit(df) # 모든 변수에 결측치 없는 데이터 추출
df_nomiss2
df
''' 분석에 필요한 데이터까지 손실 될 가능성을 유의 '''

# 함수의 결측치 제외 기능 사용 : na.rm = T
mean(df$score, na.rm = T)

# summarise 에서 na.rm = T 사용
exam <- read.csv('csv_exam.csv')
exam[c(3,8,15),'math'] <- NA # 3,8,15 행 math 에 NA 할당
exam  

exam %>% summarise(mean_math = mean(math, na.rm = T)) # 결측치 제외하고 평균 산출

### 결측치 대체
''' 
결측치가 많을 경우 모두 제외하면 데이터 손실 큼
-> 다른 값 채워넣기

결측치 대체법
- 대표값(평균, 최빈값 등)으로 일괄 대체
- 통계 분석 기법 적용, 예측값 추정해서 대체
'''

### 평균값으로 결측치 대체
mean(exam$math, na.rm=T)

# 평균으로 대체 : 55
exam$math <- ifelse(is.na(exam$math), 55, exam$math)
table(is.na(exam$math))
exam
mean(exam$math)

''' 이상치(Outlier) : 정상범주에서 크게 벗어난 값
- 이상치 포함시 분석 결과 왜곡
- 결측 처리 후 제외하고 분석

1. 존재할 수 없는 값 : 성별 변수에 3 , 년도 변수에 -> 결측 처리
2. 극단적인 값 : 몸무게 변수에 250, -> 정상범위 기준 정해서 결측 처리
'''

### 이상치 제거 - 존재할 수 없는 값

# 이상치 생성 - s 3, score 6
outlier <- data.frame(s = c(1,2,1,3,2,1),
                      score = c(5,4,3,4,2,6))
outlier

# 이상치 확인
table(outlier$s)
table(outlier$score)

# 결측 처리
outlier$s <- ifelse(outlier$s == 3, NA, outlier$s)
outlier

outlier$score <- ifelse(outlier$score > 5, NA, outlier$score)
outlier

# 결측치 제외하고 분석
outlier %>% 
  filter(!is.na(s) & !is.na(score)) %>% 
  group_by(s) %>% 
  summarise(mean_score = mean(score))

### 이상치 제거 - 극단적인 값
'''
정상범위 기준 정해서 벗어나면 결측 처리

판단 기준
1. 논리적 판단 ex) 성인 몸무게 40kg - 150kg 벗어나면 극단치로 간주
2. 통계적 판단 ex) 상하위 0.3% 극단치 또는 상자그림 1.5 IQR 벗어나면 극단치
'''

# 상자그림으로 극단치 기준 정해서 제거
mpg <- as.data.frame(ggplot2 :: mpg)
mpg
boxplot(mpg$hwy)

'''
상자 아래 세로 점선 : 아래수염 - 하위 0~25% 안에 해당하는 값
상자 밑면 : 1사분위수(Q1) - 하위 25% 에 위치하는 값
상자 내 굵은 선 : 2사분위수(Q2) - 하위 50% 위치하는 값 (중앙값)
상자 윗면 : 3사분위수(Q3) - 하위 75% 에 위치하는 값
상자 위 세로 점선 : 윗수염 - 하위 75~100% 안에 해당하는 값
상자 밖 가로선 : 극단치 경계 - Q1, Q3 밖 1.5IQR 내 최대값
상자 밖 점 표식 : 극단치 - Q1, Q3 밖 1.5IQR 을 벗어난 값
'''

# 상자 그림 통계치 출력
boxplot(mpg$hwy)$stats
'''
     [,1]
[1,]   12 -> 최소값
[2,]   18 -> 1사분위수
[3,]   24 -> 중앙값
[4,]   27 -> 3사분위수
[5,]   37 -> 최대값
'''

# 결측 처리 - 12~37 벗어나면 NA 할당
mpg$hwy <- ifelse(mpg$hwy < 12 | mpg$hwy > 37, NA, mpg$hwy)
table(is.na(mpg$hwy))

# 결측 처리 된 값을 제외하고 분석
mpg %>% 
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy, na.rm = T))

# ------------------------------------------------------------------------------
''' 그래프 '''
'''
2차원 그래프, 3차원 그래프
지도 그래프
네트워크 그래프
모션 차트
인터랙티브 그래프
'''
'''
ggplot2 의 레이어 구조 이해
1단계 : 배경 설정(축)
2단계 : 그래프 추가 (점, 막대, 선...)
3단계 : 설정 추가(축 범위, 색, 표식...)
'''

### 산점도(Scater plot) : 데이터를 x축과 y축에 점으로 표현한 그래프
# -> 나이와 소득 처럼 연속 값으로 된 두 변수의 관계를 표현할 때 사용

library(ggplot2)

# 1. 배경 설정 - x축 displ(배기량), y축 hwy(고속도로 연비) 로 지정해 배경 생성
mpg <- as.data.frame(ggplot2::mpg)
ggplot(data=mpg, aes(x=displ, y=hwy))

# 2. 그래프 추가 - 산점도
ggplot(data=mpg, aes(x=displ, y=hwy)) + geom_point()

# 3. 축 범위를 조정하는 설정 추가
ggplot(data=mpg, aes(x=displ, y=hwy)) + geom_point() + xlim(3,6) + ylim(10, 30)

# + 코드 가독성 높이기
ggplot(data=mpg, aes(x=displ, y=hwy)) + 
  geom_point() + 
  xlim(3,6) + 
  ylim(10, 30)

'''
qplot() : 전처리 단계에서 데이터 확인용 - 문법 간단, 기능 단순
ggplot() : 최종 보고용 - 색, 크기, 폰트 등 세부 조작 가능
'''

### 막대 그래프(Bar Chart) - 집단 간 차이
# -> 데이터의 크기를 막대의 길이로 표현한 그래프 
# -> 성별 소득 차이 처럼 집단 간 차이를 표현할 때 주로 사용

## 막대 그래프 1 - 평균 막대 그래프 생성

# 1. 집단별 평균표
library(dplyr)

df_mpg <- mpg %>% 
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy))
df_mpg

# 2. 그래프 생성
ggplot(data=df_mpg, aes(x=drv, y=mean_hwy)) + geom_col()

# 3. 막대 그래프 크기순으로 정렬
ggplot(data=df_mpg, aes(x = reorder(drv, -mean_hwy), y= mean_hwy)) +
  geom_col()


## 막대 그래프 2 - 빈도 막대 그래프
# -> 값의 개수(빈도)를 막대의 길이로 표현한 그래프

# x 축 범주 변수, y 축 빈도
ggplot(data = mpg, aes(x=drv)) + geom_bar()
ggplot(data = mpg , aes(x=hwy)) + geom_bar()

'''
평균 막대 그래프 : 데이터를 요약한 평균표를 먼저 만든 후 평균표를 사용해서 그래프
                  생성 - geom_col()
빈도 막대 그래프 : 별도로 표를 만들지 않고 원자료를 이용해 바로 그래프 생성
                  - geom_bar()
'''

'''
Q . mpg 데이터에서 어떤 회사에서 생산한 "suv"차종의 도시 연비가 높은지 알아보려 한다,
  "suv"차종을 대상으로 평균cty(도시 연비)가 가장 높은 회사 다섯 곳을 막대 그래프로
  표현해 보세요. 막대는 연비가 높은 순으로 정렬하세요.
'''
df <- mpg %>% 
  filter(class == 'suv') %>% 
  group_by(manufacturer) %>% 
  summarise(mean_cty = mean(cty)) %>% 
  arrange(desc(mean_cty)) %>% 
  head(5)
df

# 그래프
ggplot(data=df, aes(x=reorder(manufacturer, -mean_cty),
                    y=mean_cty)) + geom_col()

''' Q. 자동차 중에서 어떤 class 의 자동차가 가장 많은지 ? '''

ggplot(data=mpg, aes(x=class)) + geom_bar()

### 선 그래프(Line Chart) - 데이터를 선으로 표현한 그래프
'''
시계열 그래프(Time Series Chart) : 일정 시간 간격을 두고 나열된 시계열 데이터를
선으로 표현한 그래프. 환율, 주가지수 등 경제 지표가 시간에 따라 어떻게 변하는지
표현할 때 사용
'''

ggplot(data = economics, aes(x=date, y=unemploy)) + geom_line()

### 상자 그림(Box Plot) : 데이터의 분포(퍼져있는 형태)를 직사각형 상자 모양으로 표현한 그래프 
# - 분포를 알 수 있기 땜누에 평균만 볼 때보다 데이터의 특성을 좀 더 자세히 이해할 수 있음

ggplot(data=mpg, aes(x=drv, y=hwy)) + geom_boxplot()

# 1.5IQR : 사분위 범위(Q1 ~ Q3간 거리)의 1.5배

# ------------------------------------------------------------------------------

''' 한국복지패널데이터 분석 '''
'''
한국복지패널데이터
- 한국보건사회연구원 발간
- 가구의 경제활동을 연구해 정책 직원에 반영할 목적
- 2006 ~ 2015년까지 전국에 7000여가구를 선정해 매년 추적 조사
- 경제활동, 생활실태, 복지욕구 등 수천 개 변수에 대한 정보로 구성
'''

### 데이터 분석 준비

# 패키지
install.packages('foreign') # foreign 패키지 설치
library(foreign)
library(dplyr)
library(ggplot2)
library(readxl)

# 데이터 불러오기
raw_welfare <- read.spss(file = 'Koweps_hpc10_2015_beta1.sav',
                         to.data.frame = T)

# 복사본 생성
welfare <- raw_welfare

### 데이터 검토(파악)
head(welfare)
str(welfare)
summary(welfare)
'''
대규모 데이터는 변수가 많고 변수명이 코드로 되어 있어서 전체 데이터 구조를 한 눈에 파악하기 어려움
변수명을 쉬운 단어로 바꾼 후 분석에 사용할 변수들 각각 파악해야함
'''

### 변수명 수정

welfare <- rename(welfare,
                  s = h10_g3, # 성별
                  birth = h10_g4, # 태어난 연도
                  marriage = h10_g10, # 혼인 상태
                  religion = h10_g11, # 종교
                  income = p1002_8aq1, # 월급
                  code_job = h10_eco9, # 직종 코드
                  code_region = h10_reg7) # 지역 코드

''' 데이터 분석 절차
1단계 . 사용할 변수 검토 및 전처리
2단계 . 변수 간 관계 분석
'''

''' 성별에 따른 월급 차이 - 성별에 따라 월급이 다를까 ? '''
'''
1. 변수 검토 및 전처리
- 성별
- 월급

2. 변수 간 관계 분석
- 성별 월급 평균표 생성
- 그래프 생성
'''

### 변수 검토
class(welfare$s)
table(welfare$s)

### 전처리

# 이상치 확인
table(welfare$s)

# 결측치 확인
table(is.na(welfare$s))

# 성별 항목 이름 부여
welfare$s <- ifelse(welfare$s == 1, 'MALE', 'FEMALE')
table(welfare$s)
qplot(welfare$s)

### 월급 변수 검토 및 전처리
class(welfare$income)
summary(welfare$income)
qplot(welfare$income) + xlim(0, 1000)

# 이상치 처리
welfare$income <- ifelse(welfare$income %in% c(0, 9999), NA, welfare$income)
table(is.na(welfare$income))

### 성별에 따른 월급 차이 분석
s_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(s) %>% 
  summarise(mean_income = mean(income))
s_income

### 그래프 생성
ggplot(data = s_income, aes(x=s, y=mean_income)) + geom_col()

''' 나이와 월급의 관계 - 몇 살 때 월급이 가장 많을까 ? '''

### 나이 변수 검토 및 전처리
class(welfare$birth)
summary(welfare$birth)
qplot(welfare$birth)

# 결측치 확인
table(is.na(welfare$birth))

# 파생변수 생성 - 나이
welfare$age <- 2015 - welfare$birth + 1
summary(welfare$age)
qplot(welfare$age)

### 나이와 월급의 관계 분석
# 1. 나이에 따른 월급 평균표
age_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(age) %>% 
  summarise(mean_income = mean(income))
age_income

# 2. 선 그래프
ggplot(data=age_income, aes(x=age, y=mean_income)) + geom_line()

''' 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까 ? '''
'''
young - 30살 미만
middle - 30살 ~ 59살
old - 60살 이상
'''

### 파생변수 생성 - 연령대
welfare <- welfare %>% 
  mutate(ageg = ifelse(age < 30, 'young',
                       ifelse(age <= 59, 'middle', 'old')))
table(welfare$ageg)

### 연령대에 따른 월급 차이 분석
# 1. 연령대별 월급 평균표 생성
ageg_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg) %>% 
  summarise(mean_income = mean(income))
ageg_income

# 2. 시각화
ggplot(data=ageg_income, aes(x=ageg, y=mean_income)) + geom_col()

# 3. 막대 정렬 : 초 중 노 순서로
ggplot(data=ageg_income, aes(x=ageg, y=mean_income, fill = ageg)) + 
  geom_col() +
  scale_x_discrete(limits = c('young', 'middle','old'))

''' 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까? '''

#1. 연령대 및 성별 월급 평균표 생성
s_income <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg, s) %>% 
  summarise(mean_income = mean(income))
s_income

# 2. 시각화
ggplot(data=s_income, aes(x=ageg, y=mean_income, fill = s)) +
  geom_col() +
  scale_x_discrete(limits=c('young', 'middle','old'))

# 3. 막대 분리 (성별)
ggplot(data=s_income, aes(x=ageg, y=mean_income, fill = s)) +
  geom_col(position = 'dodge') +
  scale_x_discrete(limits=c('young', 'middle','old'))

### 나이 및 성별 월급 차이 분석
# 1. 성별 나이별 월급 평균표
s_age <- welfare %>% 
  filter(!is.na(income)) %>% 
  group_by(age, s) %>% 
  summarise(mean_income = mean(income))
s_age

# 2. 시각화
ggplot(data = s_age, aes(x=age, y=mean_income, col=s)) + geom_line()

''' 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까 ? '''

class(welfare$code_job)
table(welfare$code_job)

# 전처리 - 직업분류코드 목록 불러오기
list_job <- read_excel('Koweps_Codebook.xlsx', col_names = T, sheet = 2)
head(list_job)
dim(list_job)

# welfare 에 직업명 결합 - 매칭
welfare <- left_join(welfare, list_job, by='code_job')
welfare$job

job_income <- welfare %>% 
  filter(!is.na(income) & !is.na(job)) %>%
  group_by(job) %>% 
  summarise(mean_income = mean(income)) 

# 상위 10개 추출
top10 <- job_income %>% 
  arrange(desc(mean_income)) %>% 
  head(10)
top10

# 그래프 생성
ggplot(data = top10, aes(x=reorder(job, mean_income), y=mean_income, fill='skyblue')) +
  geom_col() +
  coord_flip()

# 하위 10개 추출
bottom10 <- job_income %>% 
  arrange(desc(mean_income)) %>% 
  tail(10)
bottom10

# 그래프 생성 (하위)
ggplot(data = bottom10, aes(x=reorder(job, -mean_income),
                            y=mean_income, fill = 'pink')) +
  geom_col() +
  coord_flip() +
  ylim(0, 850)

''' 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까? '''

# 남성 상위 10개 추출
job_male <- welfare %>% 
  filter(!is.na(job) & s == 'MALE') %>% 
  group_by(job) %>% 
  summarise(n = n()) %>% 
  arrange(desc(n)) %>% 
  head(10)
job_male

# 여성 상위 10개 추출
job_female <- welfare %>% 
  filter(!is.na(job) & s == 'FEMALE') %>% 
  group_by(job) %>% 
  summarise(n = n()) %>% 
  arrange(desc(n)) %>% 
  head(10)
job_female

### 시각화
# 남성
ggplot(data=job_male, aes(x=reorder(job, n), y=n)) +
  geom_col() +
  coord_flip()

# 여성
ggplot(data=job_female, aes(x=reorder(job, n), y=n)) +
  geom_col() +
  coord_flip()
