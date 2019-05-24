# 시설물 대여 시스템
## 개요
- 많은 사람들이 공통적으로 느끼고 있는 강의실 대여 시스템의 불편함을 해소해보고자 유저가 대여 현황 조회와 대여 예약을 할 수 있는 프로그램을 구상했습니다.
- 실제 통합된 시설물 대여 시스템을 구현하였고 실제로 시설물 조회, 예약, 취소 등 필요한 기능을 사용할 수 있습니다.


## 운용환경 및 준비
- Linux환경에서 MySQL, Python Flask로 동작하며 pymsql을 통해 연결됩니다.
- 웹 기반 시스템이며 마이크로소프트 엣지, 구글 크롬 브라우저를 권장합니다.
- MySQL에 아래와 같은 테이블이 필요합니다. 사전에 준비하시기 바랍니다.

> \<Tables\>  
> - users - reservations_id : int(11), user_id : varchar(45), facility_id : int(11), start_time : datetime, endtime : datetime  
> - departments - department_id : int(11), department_name : int(45), manager_name : varchar(45), department_location : varchar(45)  
> - reservations - reservations_id : int(11), user_id : int(45), facility_id : int(11), start_time : datetime, endtime : datetime  
> - facilities - facility_id : int(11), department_id : int(11), facility_type : varchar(45), capacity : int(11), location : varchar(45), location_detail : varchar(45), equipment : varchar(45)  

- 세부 제약조건과 내용은 최종보고서를 참고해주시기 바랍니다.  


## 1.설치 및 초기설정
- GIT Clone

> git clone http://khuhub.khu.ac.kr/2013104043/db-frs.git  
> cd db-frs  

- 파이썬 가상환경 만들기

> python3 -m venv env  
> source env/bin/activate  

- 파이썬 패키지 설치

> pip install flask  
> pip install pymysql  

- user_info에서 자신의 MySQL 계정과 비밀번호 설정  
- ReservationControl.py, Users.py에서 각 함수마다 DB의 호스트 주소와 사용할 DB이름을 설정

> db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd, db='dbname', charset='utf8')  

- flask서버 구동  

  
## 2.기능
- 모든 화면에서 로고를 선택하면 처음화면으로 돌아갈 수 있습니다.  

### 1) 첫 로그인 화면
- 첫 화면에서는 로그인이 가능하며, 회원가입을 통해 가입한 후 서비스를 사용할 수 있습니다.  

### 2) 메인화면
- 로그인 후 처음으로 보여지는 화면으로 '대여하기', '대여현황', '로그아웃'을 선택할 수 있습니다.  
- '대여하기'를 선택하면 대여화면으로 이동합니다.  
- '대여현황'을 선택하면 대여현황화면으로 이동합니다.  
- '로그아웃'을 선택하면 로그아웃 후 처음화면으로 돌아갑니다.  

### 3-1) 대여화면
- 사용자가 원하는 조건으로 시설물을 검색할 수 있는 화면입니다.  
- '건물'에서 사용자가 원하는 건물을 선택할 수 있습니다.  
- '사용 인원 수'에서 사용자가 원하는 규모의 시설물을 선택할 수 있습니다.  
- '시작시간'과 '종료시간'을 설정합니다.
- '검색'을 선택하여 대여가능한 시설물을 확인할 수 있습니다.  

### 3-2) 검색결과화면
- 사용자가 선택한 시간에 사용 가능한 시설물이 나타납니다.  
- '예약'을 선택하여 시설물 예약을 완료합니다.  

### 4) 대여현황화면
- 사용자가 대여한 시설물들을 확인할 수 있습니다.  
- 대여현황 옆의 각각의 버튼을 선택하여 해당 시설물의 대여를 취소할 수 있습니다.  


    
##### 기타 문의사항은 2018-2 데이터베이스 'DB아파트209호'로 연락주시고 얼마든지 가져다 쓰시면 감사하겠습니다.