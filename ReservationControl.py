# -*- coding: utf-8 -*-
# 한글 인코딩을 위한 주석입니다.

# 사전설정:
# pymysql 패키지가 있어야 합니다.
# pip install pymysql
# 보안상 user_info에서 DB id, password를 가져옵니다.
# user_info.py에서 DB id, password를 설정하고 사용해주세요.
# 외부에서 사용법:
# from ReservationControl import *

import pymysql
import user_info
import datetime


# getReservations - 대여현황반환 함수
# input:
# string user_id
# output:
# 성공시 : tuple형태로 반환 => ( (1 ,"steven123", 7, "전자정보대학", "136호", 10,  datetime.datetime(2018,12,5,12,0,0), datetime.datetime(2018,12,5,12,10,0), ), )
# 순서 : reservations_id, user_id, facility_id, location, location_detail, capacity, start_time, end_time

# 실패시 : result[0][0]="SQL Error!"인 tuple 반환 => ( ("SQL Error!", ), )
# 사용예:
# result = getReservations("khucse123")
# reservation_start_time = result[0][3]

def getReservations(user_id):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        # curs.execute("select * from reservations where user_id=%s", user_id)
        curs.execute(
            "select r.reservations_id, r.user_id, r.facility_id, f.location, f.location_detail, f.capacity, r.start_time, r.end_time from reservations r, facilities f where r.user_id=%s AND r.facility_id=f.facility_id;",
            user_id)
        result = curs.fetchall()
        print("Fetch Success!")
        return result
    except:
        print("SQL Error!")
        return (("SQL Error!",),)

    finally:
        db.close()


# deleteReservations - 대여현황삭제 함수
# input:
# int reservations_id
# output:
# 성공시 : True
# 실패시 : False
# 사용예:
# deleteReservations(5)
# 주의사항:
# 테스트환경에서 없는 reservations_id를 넣으면 에러가 날 수 있음

def deleteReservations(reservations_id):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        curs.execute("delete from reservations where reservations_id=%s", reservations_id)
        db.commit()
        print("Delete Success!")
        return True
    except:
        print("SQL Error!")
        return False

    finally:
        db.close()


# addReservations - 대여현황추가 함수
# input:
# string user_id
# int facility_id
# datetime.datetime start_time
# datetime.datetime end_time
# output:
# 성공시 : True
# 실패시 : False
# 사용예:
# tstart = datetime.datetime(2018,12,5,0,11,12)
# tend = datetime.datetime(2018,12,5,0,20,12)
# addReservations("khucse123", 6, tstart, tend)
# 주의사항:
# 테스트환경에서 없는 user_id를 넣으면 에러가 날 수 있음
# 테스트환경에서 없는 facility_id를 넣으면 에러가 날 수 있음

def addReservations(user_id, facility_id, start_time, end_time):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        curs.execute("insert into reservations (user_id, facility_id, start_time, end_time) values (%s,%s,%s,%s)",
                     (user_id, facility_id, start_time, end_time))
        db.commit()
        print("Add Reservation Success!")
        return True
    except:
        print("SQL Error!")
        return False

    finally:
        db.close()


# getAvailableFacilities - 사용가능시설물 반환함수
# input:
# string location
# int capacity
# datetime.datetime start_time
# datetime.datetime end_time
# output:
# 성공시 : tuple형태로 반환 => ( (1, "전자정보대학", "B01호", 40, "강의실", "빔프로젝터", ), )
# 순서 : facility_id, location, location_detail, capacity, facility_type, equipment
# 사용가능한 시설물이 없을 시 : result[0][0]="NoAvailableFacilites"인 tuple 반환 => ( ("NoAvailableFacilites", ), )

# 실패시 : result[0][0]="SQL Error!"인 tuple 반환 => ( ("SQL Error!", ), )
# 사용예:
# tstart = datetime.datetime(2018,12,5,12,11,12)
# tend = datetime.datetime(2018,12,5,14,20,12)
# result = getAvailableFacilities("전자정보대학", 40, tstart, tend)
# facility_id = result[0][0]

def getAvailableFacilities(location, capacity, start_time, end_time):
    try:
        db = pymysql.connect(host='host-address', port=3306, user=user_info.user_id, password=user_info.user_passwd,
                             db='dbname', charset='utf8')
        curs = db.cursor()

        curs.execute(
            "select facility_id, location, location_detail, capacity, facility_type, equipment from facilities where (facility_id not in(select facility_id from reservations where (start_time<=%s AND %s<end_time) OR (start_time<%s AND %s<=end_time) OR (%s<=start_time AND end_time<=%s))) AND location=%s AND %s<=capacity;",
            (start_time, start_time, end_time, end_time, start_time, end_time, location, capacity))

        result = curs.fetchall()
        print("Fetch Success!")

        # 사용 가능한 시설물이 있을 경우
        if (len(result) != 0):
            return result
        # 사용 가능한 시설물이 없을 경우
        else:
            print("No Available Facilities")
            return (("NoAvailableFacilities",),)

    except:
        print("SQL Error!")
        return (("SQL Error!",),)

    finally:
        db.close()
