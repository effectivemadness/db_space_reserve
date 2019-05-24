# -*- coding: utf-8 -*-
# 한글 인코딩을 위한 주석입니다.

# 사전설정:
# pymysql 패키지가 있어야 합니다.
# pip install pymysql
# 보안상 user_info에서 DB id, password를 가져옵니다.
# user_info.py에서 DB id, password를 설정하고 사용해주세요.
# 외부에서 사용법:
# from Users import *

import pymysql
import user_info


# UserLogin - 유저 로그인 함수
# input:
# string user_id
# string password
# output:
# 성공시 : True
# 실패시 : False
# 사용예:
# UserLogin("khucse124", "steven1234")

def UserLogin(user_id, password):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        curs.execute("select exists (select user_name from users where user_id=%s and password=%s) as result",
                     (user_id, password))
        result = curs.fetchall()

        if (result[0][0] == 1):
            print("User login Success!")
            return True
        else:
            print("User login Failed!")
            return False

    except:
        print("SQL ERROR!!")
        return False

    finally:
        db.close()


# UserJoin - 유저 회원가입 함수
# input:
# string user_id
# int dept_id
# string user_name
# string pwd
# string phone
# string mail
# output:
# 성공시 : True
# 실패시 : False
# 사용예:
# UserJoin("khucse124", 7, "Steven", "steven1234", "031-201-2566", "cs@khu.ac.kr")
# 주의사항:
# 테스트환경에서 같은 user_id가 있으면 에러가 날 수 있음
# 테스트환경에서 dept_id는 departments 테이블에 없는 값을 넣으면 에러가 날 수 있음

def UserJoin(user_id, dept_id, user_name, pwd, phone, mail):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        curs.execute(
            "insert into users (user_id, department_id, user_name, password, phone, mail_address) values (%s,%s,%s,%s,%s,%s)",
            (user_id, dept_id, user_name, pwd, phone, mail))
        db.commit()
        print("User Join Success!")
        return True

    except:
        print("SQL ERROR!!")
        return False

    finally:
        db.close()

