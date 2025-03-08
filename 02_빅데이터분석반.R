''' 25 - 02 - 08 강의 자료 '''

''' Review 

1. 변수(Variable) : 변하는 수
- 다양한 값을 지니고 있는 하나의 속성 (데이터)
- 분석의 대상

b <- 4

2. 함수(Function) : 기능을 하는 수
- 값을 넣으면 특정한 기능을 수행해서 처음과 다른 값을 출력하는 수

3. 패키지(Package) : 여러 함수들의 꾸러미

  패키지 설치 -> 패키지 로드 -> 함수 사용
  
- 설치 명령어  
install.packages('패키지 이름') # 괄호 안에 패키지명을 문자열로 넣어준다.

- 로드
library(패키지 이름) # 로드할 때는 문자열로 넣지 않고 그냥 패키지 명을 써준다.
'''

library(ggplot2)

x <- c('a','a','b','c','d','d','d')
qplot(x)


# ------------------------------------------------------------------------------

''' 데이터 프레임 (Data Frame) 
- 열은 속성이다.
- 행은 한 사람의 정보다.
- 데이터가 크다 -> 행 또는 열이 많다.
'''

### 데이터 입력해서 데이터 프레임 생성

english <- c(90, 80, 60, 70)
english

math <- c(50,60,100,20)
math

df_mid <- data.frame(english, math)
df_mid

# 반을 추가하고 싶을 때

class <- c(1,1,2,2)

df_mid <- data.frame(english, math, class)
df_mid

# 함수 적용
mean(df_mid$math)

### 데이터 프레임 생성을 한 번에 할 때
df_mid <- data.frame(english = c(90,80,60,70),
                     math = c(50,60,100,20),
                     class = c(1,2,3,4))
df_mid

### 외부 데이터 사용하기 - 시험 성적 데이터

# 1. 엑셀 파일 불러오기
install.packages('readxl')
library(readxl)

df_exam <- read_excel('excel_exam.xlsx') # 엑셀 파일을 읽어와서 df_exam에 할당
df_exam

mean(df_exam$science)

# 2. 직접 경로 지정
df_exam <- read_excel('c:/R_Project_mhj/excel_exam.xlsx') # 경로 + 파일명


### 엑셀 파일 첫 번째 행이 변수명이 아닌 경우?
df_novar <- read_excel('excel_exam_novar.xlsx', col_names = F)
df_novar

### 엑셀 파일에 시트가 여러 개 있다면?
df_sheet <- read_excel('excel_exam_sheet.xlsx', sheet = 3)
df_sheet

### CSV 파일 불러오기
'''
CSV 형식
- 범용 데이터 형식
- 값 사이를 쉼표(,) 로 구분
- 용량 작음, 다양한 소프트웨어에서 사용
'''

df_csv_exam <- read.csv('csv_exam.csv')
df_csv_exam

### 데이터 프레임을 csv 파일로 저장
df_mid

write.csv(df_mid, file = 'df_mid.csv')

# ------------------------------------------------------------------------------

''' 데이터 파악 '''

''' - 데이터 파악 함수

1. head() : 데이터의 앞 부분 출력
2. tail() : 데이터의 뒷 부분 출력
3. View() : 뷰어 창에서 데이터 확인 -> 잘 x
4. dim() : 데이터 차원 출력
5.** str() : 데이터의 속성 출력
6.** summary() : 요약통계량 출력
'''

### head() - 데이터 앞 부분
head(df_exam) # 앞에서부터 6행까지 출력
head(df_exam, 15) # 앞에서부터 15행까지 출력


### tail() - 데이터 뒷 부분
tail(df_exam) # 뒤에서부터 6행 출력
tail(df_exam, 10) # 뒤에서부터 10행 출력

### View() - 뷰어
View(df_exam)

### dim() - 차원 출력
dim(df_exam)

### str() - 데이터 속성 출력
str(df_exam)

### summary() - 요약통계량
summary(df_exam)

### mpg 데이터 파악하기

# 1. mpg 데이터 로드 방법 - ggplot2 의 mpg 데이터를 데이터 프레임 형태로 로드
mpg <- as.data.frame(ggplot2 :: mpg)

str(mpg)
''' int : 정수값, chr : 문자열 '''
summary(mpg)

### 데이터 수정 - 변수명 바꾸기

# dplyr 패키지 설치 & 로드
install.packages('dplyr')
library(dplyr)

# 1. 예제 생성
df_raw <- data.frame(var1 = c(1,2,1),
                     var2 = c(2,3,2))
df_raw

# 2. 데이터 프레임 복사본 생성 - 원본 데이터 손실 방지
df_new <- df_raw
df_new

# 3. 변수명 수정 - 유의할 점 : 새 변수명 = 기존 변수명 순서로 입력을 한다.
df_new <- rename(df_new, v2 = var2) # var2를 v2로 수정
df_new

### 파생변수 생성 - 기존에 존재하는 변수를 활용해서 새로 만드는 변수

# 1. 변수를 조합해서 파생변수 생성
df <- data.frame(var1 = c(4,3,8),
                 var2 = c(2,6,1))
df

df$var_sum <- df$var1 + df$var2
df

df$var_mean <- (df$var1 + df$var2)/2
df


# 2. mpg 데이터에서 통합 연비 변수 생성
mpg$total <- (mpg$cty + mpg$hwy)/2
head(mpg)

mean(mpg$total)

# 3. 조건문을 활용해서 파생변수 생성 - 합격 판정 변수 생성

# 3-1. 기준값 정하기 - 히스토그램 활용
summary(mpg$total)
hist(mpg$total) # 통합 연비 기준을 25 로 결정

# 3-2. 조건문으로 합격 판정 변수 생성
# -> 25 이상이면 PASS , 그렇지 않으면 FAIL 부여
mpg$test <- ifelse(mpg$total >= 25, 'PASS', 'FAIL')
head(mpg, 20)

# 3-3. 빈도표로 합격 판정 자동차 수 살펴보기
table(mpg$test)

# 3-4. 막대그래프로 빈도 표현
library(ggplot2)
qplot(mpg$test)

# 4. 중첩 조건문 - 연비 등급 변수 생성
'''
30 이상 - A 등급
20~29 - B 등급
20 미만 - C 등급
'''

mpg$grade <- ifelse(mpg$total >= 30, 'A',
                    ifelse(mpg$total >= 20,'B','C'))
head(mpg, 15)
tail(mpg, 20)

table(mpg$grade)
qplot(mpg$grade)

# ------------------------------------------------------------------------------

''' 데이터 가공 - 데이터 전처리 : 원하는 형태로 데이터를 가공 '''
'''
데이터 전처리(Preprocessing) - dplry 패키지

1. filter() : 행 추출
2. select() : 열 추출
3. arrange() : 정렬
4. mutate() : 변수 추가
5. summarise() : 통계치 산출
6. group_by() : 집단별로 나누기 (군집화)
7. left_join() : 데이터 합치기 (열 기준)
8. bind_rows() : 데이터 합치기 (행 기준)
'''

### 조건에 맞는 데이터만 추출 - filter()
exam <- read.csv('csv_exam.csv')
exam

# class 가 1인 경우만 추출
exam %>% filter(class == 1)

'''
1. %>% : 파이프 기호 -> df 와 dplyr 패키지 함수를 연결 / 단축키 [Ctrl + Shift + M]
2. 조건문에서 같다는 등호를 == 두 번 쓴다.
'''

# 1반이 아닌 경우
exam %>% filter(class != 1) # != : 아닌 경우 

# 초과, 미만, 이상, 이하 조건 
exam %>% filter(math >= 50)

# 여러 조건을 충족하는 행 추출
exam %>% filter(class == 1 & math >= 50) # 1반 안에서 수학점수가 50점 이상인 학생만 추출

# 여러 조건 중 하나 이상 만족하는 행 추출
exam %>% filter(math >= 90 | english >= 90) # 수학 점수가 90점 이상이거나 영어 점수가 90점 이상인 경우

# 목록에 해당되는 행 추출 - %in% 기호

exam %>% filter(class == 1 | class == 3 | class == 5) # 1, 3, 5반에 해당되면 추출
exam %>% filter(class %in% c(1,3,5))

# 추출한 행으로 데이터를 만들기
class1 <- exam %>% filter(class == 1)
class2 <- exam %>% filter(class == 2)

mean(class1$math)
mean(class2$math)

'''
R 에서 사용하는 기호

1. 논리 연산자
- < : 작다
- <= : 작거나 같다
- > : 크다
- >= : 크거나 같다
- == : 같다
- != : 같지 않다
- | (버티컬 바) : 또는
- & : 그리고
- %in% : 포함 연산자, 매칭 확인

2. 산술 연산자
- + : 더하기
- - : 빼기
- * : 곱하기
- / : 나누기
- ^, ** : 제곱
- %/% : 나눗셈의 몫
- %% : 나눗셈의 나머지
'''

### 필요한 변수만 추출 - select()

exam %>% select(math)

# 여러 변수 추출
exam %>% select(class, math, science)

# 변수 제외
exam %>% select(-math)

### dplry 함수들 조합

# class 가 1인 행만 추출한 다음 english 만 추출
exam %>% filter(class == 1) %>% select(english)

# 가독성 있게 코드 변경
exam %>% 
  filter(class == 1) %>% 
  select(math, english) %>% 
  head(2)

### 순서대로 정렬 - arrange()

# 오름차순
exam %>% arrange(math)

# 내림차순
exam %>% arrange(desc(math)) # descent : 내려오기

'''
Q . mpg 데이터에서 'audi' 에서 생산한 자동차중에 어떤 자동차 모델이 hwy 가 높은지 1~5등까지 출력하세요
'''
mpg

mpg %>% filter(manufacturer == 'audi') %>% 
  arrange(desc(hwy)) %>% 
  head(5)

### 파생변수 추가 - mutate()

exam <- read.csv('csv_exam.csv')

exam %>% 
  mutate(total = math + english + science)

exam


# 파생변수 한 번에 추가
exam %>% 
  mutate(total = math + english + science,
         mean = (math + english + science)/3)

# mutate에 ifelse 적용 가능
exam %>% 
  mutate(test = ifelse(science >= 60, 'PASS', 'FAIL'))

# 추가한 변수를 dplyr 코드에 바로 적용 가능
exam %>% 
  mutate(total = math + english + science) %>% 
  arrange(desc(total)) %>% 
  head(10)

### 집단별로 요약 - group_by() , summarise()

# 요약하기 - 전체 학생의 수학 평균을 구하시오.
exam %>% summarise(mean_math = mean(math))

# 집단별로 요약하기 - 반 별 수학 점수 평균을 내시오.
exam %>% 
  group_by(class) %>% 
  summarise(mean_math = mean(math))

# 여러 요약통계량 한 번에 산출 가능
exam %>% 
  group_by(class) %>%
  summarise(mean_math = mean(math),
            sum_math = sum(math),
            median_math = median(math),
            n = n())

''' 자주 쓰는 요약통계량 함수
1. mean() : 평균
2. sd() : 표준편차
3. sum() : 합계
4. median() : 중앙값
5. min(), max() : 최소, 최대
6. n() : 빈도
'''

'''
Q. mpg 데이터에서 회사별로 
"suv" 자동차의 
도시 및 고속도로 통합 연비 평균을 구해서
내림차순으로 정렬하고, 
1~5위까지 출력
'''
mpg <- as.data.frame(ggplot2 :: mpg)
mpg

mpg %>% group_by(manufacturer) %>% 
  filter(class == 'suv') %>% 
  mutate(tot = (cty + hwy)/2) %>% 
  summarise(mean_tot = mean(tot)) %>%
  arrange(desc(mean_tot)) %>% 
  head(5)

### 데이터 합치기 - 가로로 합치기, 세로로 합치기

# 1. 가로로 합치기 - left_join()

test1 <- data.frame(id = c(1,2,3,4,5),
                    midterm = c(60,80,70,90,50))

test2 <- data.frame(id = c(1,2,3,4,5),
                    final = c(70,83,65,95,80))

test1
test2

# 1-2. id 기준으로 합치기
total <- left_join(test1, test2, by='id')
total

## 다른 데이터 활용해서 변수 추가하기 - 매칭
name <- data.frame(class = c(1,2,3,4,5),
                   teacher = c('kim','lee','park','choi','jung'))
name
exam

# 1. class 기준으로 합치기
exam_new <- left_join(exam, name, by='class')
exam_new

### 세로로 합치기 - bind_rows()

group_a <- data.frame(id = c(1,2,3,4,5),
                      score = c(60,80,70,90,85))

group_b <- data.frame(id = c(6,7,8,9,10),
                      score = c(70,83,65,98,80))
group_a
group_b

group_all <- bind_rows(group_a, group_b)
group_all
