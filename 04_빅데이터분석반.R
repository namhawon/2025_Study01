''' 25 - 02 - 22 강의 자료 공유 '''

''' 종교 유무에 따른 이혼율 - 종교가 있는 사람들이 이혼을 덜 할까 ? '''

### 종교 변수 검토 및 전처리
library(foreign)
library(dplyr)
library(readxl)

welfare <- read.spss('Koweps_hpc10_2015_beta1.sav',
                     to.data.frame = T)

welfare <- rename(welfare,
                  s = h10_g3,
                  birth = h10_g4,
                  marriage = h10_g10,
                  religion = h10_g11,
                  income = p1002_8aq1,
                  code_job = h10_eco9,
                  code_region = h10_reg7)

class(welfare$religion)
library(ggplot2)
qplot(welfare$religion)

### 혼인 상태 변수 검토 및 전처리
class(welfare$marriage)
table(welfare$marriage)

# 1. 이혼 여부 변수 만들기
welfare$group_marriage <- ifelse(welfare$marriage == 1, 'marriage',
                                 ifelse(welfare$marriage == 3, 'divorce', NA))
table(welfare$group_marriage)
table(is.na(welfare$group_marriage))
qplot(welfare$group_marriage)


# 2. 종교 유무에 이름 부여
welfare$religion <- ifelse(welfare$religion == 1, '종교 있음', '종교 없음')
table(welfare$religion)
### 종교 유무에 따른 이혼율 분석

religion_marriage <- welfare %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(religion, group_marriage) %>% 
  summarise(n = n()) %>% 
  mutate(total_group = sum(n),
         pct = round(n/total_group*100, 1))
religion_marriage

# 이혼율 표 출력
divorce <- religion_marriage %>% 
  filter(group_marriage == 'divorce') %>% 
  select(religion, pct)
divorce

# 그래프
ggplot(data = divorce, aes(x=religion, y=pct, fill=religion)) + geom_col()

''' 지역별 연령대 비율 - 노년층이 제일 많은 지역이 어딜까 ? '''

welfare$age <- 2015 - welfare$birth + 1 

welfare <- welfare %>% 
  mutate(ageg = ifelse(age < 30, 'young',
                       ifelse(age <= 59, 'middle', 'old')))
table(welfare$ageg)

### 지역 변수 검토 및 전처리
class(welfare$code_region)
table(welfare$code_region)

# 1. 지역 코드 목록 생성
list_region = data.frame(code_region = c(1:7),
                         region = c('서울',
                                    '수도권(인천/경기)',
                                    '부산/울산/경남',
                                    '대구/경북',
                                    '대전/충남',
                                    '강원/충북',
                                    '광주/전남/전북/제주도'))
list_region

# 2. welfare 에 지역명 변수 추가
welfare <- left_join(welfare, list_region, by='code_region')

welfare %>% 
  select(code_region, region) %>% 
  head(20)

### 지역별 연령대 비율 분석
region_ageg <- welfare %>% 
  group_by(region, ageg) %>% 
  summarise(n = n()) %>% 
  mutate(tot_group = sum(n),
         pct = round(n/tot_group*100, 2))
region_ageg

### 그래프
ggplot(data=region_ageg, aes(x=region, y=pct, fill=ageg)) +
  geom_col() +
  coord_flip()

# 1. 막대 정렬 : 노년층 비율 낮은 순
# 노년층 비율 오름차순 정렬
list_order_old <- region_ageg %>% 
  filter(ageg == 'old') %>% 
  arrange(pct)
list_order_old  

# 지역명 순서 변수 만들어 놓기 -> 그래프의 입력값으로 줄려고
order <-  list_order_old$region
order

ggplot(data = region_ageg, aes(x=region, y=pct, fill=ageg)) +
  geom_col() +
  coord_flip() +
  scale_x_discrete(limits = order)

# 연령대 순으로 막대 색깔 나열하기
class(region_ageg$ageg)
levels(region_ageg$ageg)

region_ageg$ageg <- factor(region_ageg$ageg,
                           level = c('old','middle','young'))
class(region_ageg$ageg)
levels(region_ageg$ageg)

ggplot(data = region_ageg, aes(x=region, y=pct, fill=ageg)) +
  geom_col() +
  coord_flip() +
  scale_x_discrete(limits = order)

# ------------------------------------------------------------------------------

''' 텍스트 마이닝 (Text mining)
 - 문자로 된 데이터에서 가치 있는 정보를 얻어 내는 분석 기법 
 - SNS나 웹 사이트에 올라온 글을 분석해 사람들이 어떤 이야기를 나누고 있는지
   파악할 때 활용
 
 - 형태소 분석 : 문장을 구성하는 어절들이 어떤 품사로 되어 있는지 분석
 - 분석 절차 
  1. 형태소 분석
  2. 명사, 동사, 형용사 등 의미를 지닌 품사의 단어를 추출
  3. 빈도표 생성
  4. 시각화
'''

''' 텍스트 마이닝 세팅법
1. java 설치 - jdk , jre
2. 시스템 환경 변수 편집
  1) 돋보기 - 시스템 환경 변수 편집 - 시스템 속성 -  환경변수
  2) JAVA_HOME, path 에 경로 삽입
3. 패키지 설치
install.packages("rJava")
install.packages("memoise")
4. KoNLP 수동 설치
카페 다운로드 - 

'''
install.packages('rJava')
install.packages('memoise')
install.packages('Sejong')
install.packages('hash')
install.packages('tau')
install.packages('RSQLite')
install.packages('devtools')
library(KoNLP)
useNIADic() # 사전
extractNoun('안녕하세요 빅데이터 분석 강의입니다.')

### 가사 텍스트 마이닝

# 1. 데이터 로드 (txt)
txt <- readLines('sung.txt')
head(txt)

# 2. 특수문자 제거
install.packages('stringr')
library(stringr)

txt <- str_replace_all(txt, '\\W',' ') # 특수문자를 공백 한 칸 으로 바꿔줌

# 3. 명사 추출 - extractNoun()
extractNoun('미련하게 아무도 모를것 같아')

# 4. 가사에서 명사 추출
nouns <- extractNoun(txt)
nouns

# 5. 추출한 명사 list를 문자열 벡터로 변환, 단어별로 빈도표 작성
wordcount <- table(unlist(nouns))
wordcount

# 6. 자주 사용된 단어 빈도표 만들기

# 데이터 프레임으로 변환
df_word <- as.data.frame(wordcount, stringsAsFactors = F)
df_word

# 변수명 수정
df_word <- rename(df_word,
                  word = Var1,
                  freq = Freq)

# 두 글자 이상 단어만 추출 기준으로 상위 20개 추출
df_word <- filter(df_word, nchar(word) >= 2)
class(df_word$word)
head(df_word)

top20 <- df_word %>% 
  arrange(desc(freq)) %>% 
  head(20)
top20  



# 7. 워드 클라우드 : 단어 구름 시각화
install.packages('wordcloud')
library(wordcloud)
library(RColorBrewer) # 글자 색 표현 패키지

# 7-1. 단어 색상 목록 코드
a <- brewer.pal.info
a

pal <- brewer.pal(8, 'Dark2') # Dark2 색상 목록에서 8개 색상 추출  

# 7-2 난수 고정 - 워드클라우드가 실행될 때마다 동일한 워드클라우드를 생성하기 위해  
set.seed(1234)  
  
# 7-3. 워드클라우드 생성
wordcloud(words = df_word$word, # 단어 입력
          freq = df_word$freq, # 빈도 입력
          min.freq = 2, # 최소 단어 빈도
          max.words = 200, # 표현 단어 수
          random.order = F, # 고빈도 단어를 중앙에 배치
          scale = c(5, 0.5), # 단어 크기 범위
          colors = pal) # 색상

''' 국정원 계정 트윗 텍스트 마이닝 

국정원 계정 트윗 데이터
-> 국정원 대선 개입 사실이 밝혀져서 논란이 되었던 13년 6월,
   독립 언론 뉴스타파 인터넷을 통해 공개된 데이터
'''

# 1. 데이터 로드
twitter <- read.csv('twitter.csv',
                    header = T,
                    stringsAsFactors = F,
                    fileEncoding = 'UTF-8') # cp949, EUC-KR
head(twitter, 5)

# 2. 변수명 수정
twitter <- rename(twitter,
                  no = 번호,
                  id = 계정이름,
                  date = 작성일,
                  tw = 내용)

# 3. 특수문자 제거
twitter$tw <- str_replace_all(twitter$tw, '\\W',' ')
head(twitter$tw)

# 4. 명사 추출
nouns <- extractNoun(twitter$tw)
head(nouns)

# 5. 추출한 명사 list를 문자열 벡터로 변환, 단어 빈도표 생성
wordcount <- table(unlist(nouns))
wordcount

# 6. 데이터 프레임으로 변환
df_word <- as.data.frame(wordcount, stringsAsFactors = F)
df_word

# 7. 변수명 수정
df_word <- rename(df_word,
                  word = Var1,
                  freq = Freq)

# 8. 두 글자 이상으로 된 단어 추출, 빈도 기준 상위 20 추출
df_word <- filter(df_word, nchar(word) >= 2)
class(df_word$word)

top20 <- df_word %>% 
  arrange(desc(freq)) %>% 
  head(20)
top20

# 9. 워드클라우드 생성
pal <- brewer.pal(9, 'Blues')[5:9]
set.seed(1234)

wordcloud(words = df_word$word,
          freq = df_word$freq,
          min.freq = 10,
          max.words = 200,
          random.order = F,
          rot.per = .1,
          scale = c(11, 0.2),
          colors = pal)
# ------------------------------------------------------------------------------

''' 인터랙티브 그래프 - plotly 패키지 '''

### 패키지 준비
install.packages('plotly')
library(plotly)

### ggplot으로 그래프 만들기
library(ggplot2)

p <- ggplot(data=mpg, aes(x=displ, y=hwy, col=drv)) + geom_point()
p

### 인터랙티브 그래프로 생성
ggplotly(p)

### 인터랙티브 막대 그래프 생성
p <- ggplot(data = diamonds, aes(x=cut, fill=clarity)) +
  geom_bar(position = 'dodge')
ggplotly(p)

### dygraphs 패키지로 인터랙티브 시계열 그래프 생성

install.packages('dygraphs')
library(dygraphs)

# 데이터 준비
economics <- ggplot2 :: economics
head(economics)

# 시간 순서 속성을 지니는 xts 데이터 타입으로 변경
library(xts)

eco <- xts(economics$unemploy, order.by = economics$date)
head(eco)

# 인터랙티브 시계열 그래프 생성
dygraph(eco)

# 날짜 범위 선택 기능 추가
dygraph(eco) %>% dyRangeSelector()

### 여러값 표현

# 저축률
eco_a <- xts(economics$psavert, order.by = economics$date)
# 실업자 수
eco_b <- xts(economics$unemploy/1000, order.by = economics$date)

# 합치기
eco2 <- cbind(eco_a, eco_b) # 데이터 결합
colnames(eco2) <- c('psavert', 'unemploy')
head(eco2)

# 그래프 생성
dygraph(eco2) %>% dyRangeSelector()

# ------------------------------------------------------------------------------

''' 통계적 가설 검정 

기술 통계와 추론 통계

- 기술 통계
 -> 데이터를 요약해서 설명하는 통계 기법
 -> ex) 사람이 받는 월급을 집계해서 전체 월급 평균 구하기
 
- 추론 통계
 -> 단순히 숫자를 요약하는 것을 넘어 어떤 값이 발생할 확률을 계산하는 통계 기법
 -> ex) 우리 데이터에서 성별에 따라 월급에 차이가 있는걸로 나타났을 때,
        이런 차이가 우연히 발생할 확률 계산


  -> 이런 차이가 우연히 나타날 확률이 작다
    -> 성별에 따른 월급 차이가 통계적으로 유의하다고 결론

  -> 이런 차이가 우연히 나타날 확률이 크다
    -> 성별에 따른 월급 차이가 통계적으로 유의하지 않다고 결론
    
  -> 기술 통계 분석에서 집단 간에 차이가 있는 것으로 나타나더라도 이는 우연에 의한
     차이일 수 있음.
     -> 데이터를 사용해서 신뢰할 수 있는 결론을 내리려면 "유의확률"을 계산하는
        통계적 가설 검정 절차를 진행해야 한다.

- 통계적 가설 검정 : 유의확률을 사용해서 가설을 검정하는 방법

- 유의확률(p-value) : 실제로는 집단 간 차이가 없는데 우연히 차이가 있는 데이터가
                      추출될 확률

  -> 분석 결과 유의확률이 크게 나타났다면
    1. 집단 간 차이가 통계적으로 유의하지 않다. 고 해석
    2. 실제로 차이가 없더라도 우연에 의해 이 정도의 차이가 괄찰될 가능성이 크다

  -> 분석 결과 유의확률이 작게 나타났다면
    1. 집단 간 차이가 통계적으로 유의하다. 고 해석
    2. 실제로 차이가 없는데 우연히 이 정도의 차이가 관찰될 가능성이 작다.
      즉, 우연으로 보기 힘들다.
'''

### t 검정 : 두 집단의 평균 비교
# -> 두 집단의 평균에 통계적으로 유의한 차이가 있는지 알아볼 때 사용하는 통계 분석 기법

### compact 자동차, suv 자동차의 도시 연비 t 검정

mpg <- as.data.frame(ggplot2::mpg)
library(dplyr)

mpg_diff <- mpg %>% 
  select(cty, class) %>% 
  filter(class %in% c('compact', 'suv'))
head(mpg_diff)
table(mpg_diff$class)

# t-test
t.test(data=mpg_diff, cty~class, var.equal = T)

# 해석법

'''
유의확률의 보편적인 기준 : 0.05

p-value < 2.2e-16 

-> 유의확률이 2.2e-16 으로 0.05보다 작다. 그러므로 compact 차와 suv차의 도시 연비 차이는
   통계적으로 유의하다. 즉, 이러한 도시연비 차이는 우연이라고 보기 힘들다.

sample estimates:
mean in group compact     mean in group suv 
             20.12766              13.50000 

-> compact 자동차의 도시연비 평균은 20 으로 나오고 suv는 13 으로 나온다. 결론은 compact 차가
  suv 차보다 도시연비가 좋다.
'''

### 일반 휘발유와 고급 휘발유의 도시 연비 t 검정

mpg_diff2 <- mpg %>% 
  select(fl, cty) %>% 
  filter(fl %in% c('p','r'))

table(mpg_diff2$fl)

# t-test
t.test(data=mpg_diff2, cty~fl, var.equal = T)

'''
p-value = 0.2875 

-> 유의확률이 0.2875 로 유의수준 0.05보다 크다. 그러므로 일반 휘발유와 고급 휘발유의
  도시 연비 차이는 통계적으로 유의하지 않다고 볼 수 있다. 즉, 일반 휘발유와 고급 휘발유의
  도시 연비 차이는 유연일 확률이 크다.
  
sample estimates:
mean in group p mean in group r 
       17.36538        16.73810 
       
'''

### 상관분석 - 두 변수가 서로 관련이 있는지 검정하는 통계 분석 기법

'''
상관 계수 (Correlation Coefficient)
- 두 변수가 얼마나 관련되어 있는지, 관련성의 정도를 나타낸 값
- 0~1 사이의 값을 지니고, 1에 가까울수록 관련성이 크다는 의미
- 상관계수가 양수면 정비례, 음수면 반비례
'''

## 실업자 수와 개인소비지출의 상관관계

economics <- as.data.frame(ggplot2::economics)

# 상관분석
cor.test(economics$unemploy, economics$pce)

# 해석
''' 
p-value < 2.2e-16 

-> 유의확률이 2.2e-16 이므로 유의수준 0.05보다 작다. 그러므로 이러한 상관은 통계적으로 유의하다.

sample estimates:
      cor 
0.6145176 

-> 상관계수가 0.614로 양수다. 실업자수와 개인소비지출은 정비례 관계이며 실업자 수가 증가하면
  개인소비지출도 증가한다.
'''

### 상관행렬 히트맵
# - 여러 변수 간 상관계수를 행렬로 나타낸 표
# - 어떤 변수끼리 관련이 크고 적은지 파악할 수 있음


# 데이터 준비
mtcars


# 상관행렬 생성
car_cor <- cor(mtcars)
round(car_cor, 2)

# 상관행렬 히트맵 : 값의 크기를 색깔로 표현한 그래프
install.packages('corrplot')
library(corrplot)

corrplot(car_cor)

# 원 대신에 상관 계수 표시
corrplot(car_cor, method = 'number')

# 다양한 파라미터 지정
col <- colorRampPalette(c('#BB4444','#EE9988','#FFFFFF','#77AADD','#4477AA'))

corrplot(car_cor,
         method = 'color', # 색깔로 표현
         col = col(200), # 색상 200개 선정
         type = 'lower', # 왼쪽 아래 행렬만 표시
         order = 'hclust', # 유사한 상관계수끼리 군집화
         addCoef.col = 'black', # 상관계수 색깔
         tl.col = 'black', # 변수명 색깔
         tl.srt = 45, # 변수명 45도 기울임
         diag = F) # 대각 행렬 제외

# ------------------------------------------------------------------------------
''' 나이브 베이즈 분류 '''

''' 기계 학습 분야에서 나이브 베이즈는 특성들 사이의 독립을 가정하는
    베이즈 정리를 적용한 확률 분류기의 일종 '''

''' tm 패키지 : 텍스트 마이닝 패키지 '''

install.packages('tm')
library(tm)

### 데이터 로드
sms_raw <- read.csv('sms_spam.csv',
                    stringsAsFactors = F)

str(sms_raw)

table(sms_raw$type)

sms_corpus <- VCorpus(VectorSource(sms_raw$text))
''' tm 패키지의 기능 : 텍스트 문서를 copus로 변환하는 함수
copus : 언어 모음을 만들어 놓은 것 '''
sms_corpus

inspect(sms_corpus[1:2])
as.character(sms_corpus[[1]])  # 1 위치 값을 문자형을 바꿔서 지정
lapply(sms_corpus[1:2], as.character)
# lapply : 벡터, 리스트, 표현식, df 등에 함수를 적용하고 그 결과를 리스트로 반환해주는 함수


















