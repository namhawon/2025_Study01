''' 25 - 02 - 01 강의 자료 '''

'''
주석 : 코드 실행에 영향을 미치지 않는 텍스트
-> 코드에 대한 설명을 쓰거나 하고자 하는 말을 코드 중간에 넣을 때

한줄 주석 : #
장문 주석 : 따옴표
-> 따옴표로 시작이되면 따옴표로 마무리가 되어야 한다.

실행 단축키 : Ctrl + Enter
'''

# 함수라고 하면 괄호가 따라온다.

### 벡터 - c() 생성
ex_vector1 <- c(-1, 0 ,1)
ex_vector1

# 데이터 구조간 관계 확인 함수 - 숫자형
mode(ex_vector1) # 데이터 유형 확인
str(ex_vector1) # 데이터 유형과 값을 전체적
length(ex_vector1) # 데이터 길이

str('Hello!')

# 문자형 벡터 : 문자로 이루어진 데이터
ex_vector2 <- c('Hello', 'Hi~!')
ex_vector2
ex_vector3 <- c('1','2','3')
ex_vector3

str(ex_vector3)

# 논리형 벡터 : TRUE 혹은 FALSE 로 이루어진 데이터 
ex_vector4 <- c(TRUE, FALSE, TRUE, FALSE)
str(ex_vector4)

### 범주형 자료 - factor()

# 1. 범주화 할 자료 생성
ex_vector5 <- c(2,1,3,2,1)

cate_vector5 <- factor(ex_vector5, labels = c('APPLE','BANANA','CHERRY'))
cate_vector5

### 행렬 - matrix()
x <- c(1,2,3,4,5,6)
matrix(x, nrow = 2, ncol = 3)
matrix(x, nrow = 3, ncol = 2)

# 옵션 추가 - byrow : 데이터를 왼쪽에서 오른쪽 열 방향으로 채운다는 옵션
matrix(x, nrow = 2, ncol = 3, byrow = T)

### 배열 - array()
y <- c(1,2,3,4,5,6)
array(y, dim = c(2, 2, 3))

### 리스트 : 1차원, 다중형 데이터 - list()

list1 <- list(c(1,2,3), "Hello")
list1

### 데이터 프레임 : 리스트를 2차원으로 확대 - data.frame()
'''
행 : 데이터 세트의 가로 영역, 관측치라고도 한다.
열 : 변수 라 부른다.
값 : 관측된 값
'''

# 데이터 프레임 생성
ID <- c(1,2,3,4,5,6,7,8,9,10)
SEX <- c('F','M','F','M','M','F','F','F','M','F')
AGE <- c(50,40,28,50,27,23,56,47,20,38)
AREA <- c('서울', '경기','제주','서울','서울','서울','경기','서울',
          '인천','경기')

dataframe_ex <- data.frame(ID, SEX, AGE, AREA)
dataframe_ex

str(dataframe_ex)

# ------------------------------------------------------------------------------

''' 변수(Variable)
- 다양한 값을 지니고 있는 하나의 속성 (데이터)
- 데이터 분석의 대상
'''

a <- 1
b <- 2
c <- 3
d <- 3.5

# 변수로 연산
a+b
5*d

# 여러 값으로 구성된 변수 생성
var1 <- c(1,2,5,7,8)
var1

var2 <- c(1:100) # 1부터 100까지 연속값으로 var2 생성
var2

data <- data.frame(var2)
data

# seq() : 생성 함수
var3 <- seq(1, 5) # 1~5 까지 연속값으로 var3 생성
var3

var4 <- seq(1, 100, by=2) # 1~100 까지 홀수값으로 생성
var4

var5 <- seq(2, 100, by=2) # 1~100 사이 짝수값으로 생성
var5

# 연속값 변수로 연산
var1

var1+2

var1 + var2

# 문자로 된 변수 생성
str1 <- 'a'
str1

str2 <- 'text'
str2

str3 <- 'Hello World!'
str3

# 연속 문자 변수 생성
str4 <- c('a','b','c')
str4

str5 <- c('Hello!','World', 'is','good!')
str5

# 문자로 된 변수로는 연산을 할 수 없다.
str1 + 2

str1 + str2

# ------------------------------------------------------------------------------
''' 함수(Function) : 기능을 하는 수
- 값을 넣으면 특정한 기능을 수행해서 처음과 다른 값을 출력하는 수
- 입력을 받아 출력을 내는 수
'''

# 숫자를 다루는 함수 사용

x <- c(1,2,3)
x

mean(x) # 평균 함수
max(x) # 최대값
min(x) # 최소값

# 문자를 다루는 함수 사용
str5

# 함수의 결과로 새로운 변수 생성 <- 잘 활용하는게 좋다.
result <- paste(str5, collapse = ',') # 쉼표를 구분자로 str4의 단어들 하나로 합치기
result

# -------------------------------------------------------------------------------

''' 패키지(Package)
- 함수가 여러 개 들어 있는 꾸러미
- 하나의 패키지 안에 다양한 함수가 들어 있음
- 함수를 사용하려면 패키지 설치가 먼저 선행되야함


      패키지 설치하기 -> 패키지 로드 -> 함수 사용

'''

# 패키지 설치 명령어
install.packages('ggplot2')
library(ggplot2) # 패키지 로드 명령어 (괄호 안에 따옴표 입력 x)

# 패키지 함수 사용 - ggplot2
x <- c('a','a','b','c')
qplot(x) # 빈도 그래프 출력 함수

# ggplot2 의 mpg 데이터로 그래프 만들기
'''
어떤 패키지에는 패키지 함수들을 써볼 수 있는 테스트용 데이터가 존재한다.
ggplot2 에는 mpg 라는 미국 자동차 데이터가 존재 한다. 
'''
qplot(data=mpg, x=hwy)

mpg = ggplot2::mpg

# qplot 파라미터 변경
# x 축 : drv (구동방식), y축 : hwy(고속도로 연비)
qplot(data=mpg, x=drv, y=hwy)
qplot(data=mpg, x=drv, y=hwy, geom = 'line')

