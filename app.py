# -*- coding: utf8 -*-
from flask import request, render_template, redirect, session, flash, Flask
from Users import *
from ReservationControl import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', redirect_to="/login")
def http_prepost_response():
    return "helloworld"


@app.route('/login', methods=["GET"])
def login():
    if session.get('ID'):
        return redirect('/myhome')
    elif request.args.get('retry') == 'true':
        return render_template("login.html", retry=True)
    return render_template("login.html", retry=False)


@app.route('/join')
def join():
    return render_template('join.html')


@app.route('/join/confirm', methods=['POST'])
def join_confirm():
    join_item = request.form
    print(join_item)
    if UserJoin(join_item.get('id'),join_item.get('deptid'),join_item.get('name'),join_item.get('password'),join_item.get('phone'),join_item.get('email')):
        flash('회원가입 성공!')
        return redirect('/login')
    flash('회원가입 실패!')
    return redirect('/join')


@app.route('/logincheck', methods=["POST"])
def login_check():
    IDPW = request.form
    if UserLogin(IDPW.get('id'),IDPW.get('pw')):
        session['ID'] = IDPW.get('id')
        welcome = IDPW.get('id')+" 님 안녕하세요!"
        flash(welcome)
        return redirect('/myhome')
    flash("ID와 비밀번호를 확인해주세요.")
    return redirect('/login?retry=true')


@app.route('/myhome')
def mystat():
    return render_template("myhome.html", ID=session['ID'])


@app.route('/viewresv')
def view_resv():
    resv_list = getReservations(session['ID'])
    print(resv_list)
    return render_template('resv_view.html', resv_list=resv_list)

@app.route('/deleteresv', methods=['POST'])
def delete_resv():
    resv_id = request.form
    if deleteReservations(resv_id.get('resv_id')):
        flash("예약이 삭제되었습니다")
    else:
        flash("예약 삭제에 실패했습니다")
    return redirect('/viewresv')



@app.route('/search')
def book():
    return render_template("resv_sch.html", ID=session['ID'])


@app.route('/search/result', methods=['POST'])
def search_result():
    searchdata = request.form
    starttime = datetime.strptime(searchdata.get('starttime'),'%Y-%m-%dT%H:%M')
    endtime = datetime.strptime(searchdata.get('endtime'),'%Y-%m-%dT%H:%M')
    if(starttime.strftime('%Y%m%d') == endtime.strftime('%Y%m%d')):
        result = getAvailableFacilities(searchdata.get('deptid'),searchdata.get('capacity'),starttime,endtime)
        print(result)
        return render_template("searchresult.html", resv_list=result, starttime=starttime, endtime=endtime)
    else:
        flash("2일 이상의 일정으로 예약 불가합니다")
        return redirect("/search")



@app.route('/search/resv', methods=['POST'])
def book_confirm():
    book_query=request.form
    print(book_query)
    starttime = datetime.strptime(book_query.get('start_time'), '%Y-%m-%d%H:%M')
    endtime = datetime.strptime(book_query.get('end_time'), '%Y-%m-%d%H:%M')
    if addReservations(session['ID'],book_query.get('fac_id'),starttime,endtime):
        flash("예약에 성공했습니다")
        return redirect('/myhome')
    else:
        flash("예약에 실패했습니다.")
        return redirect('/search')




@app.route('/logout')
def logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect('/login')


if __name__ == '__main__':

    print("done")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=80)
