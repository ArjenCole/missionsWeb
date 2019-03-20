from django.shortcuts import render
from missions import db
import hashlib
import base64
# Create your views here.


def index(request):
    # data = db.query("Password", "staffs", "Account", "jinhe@smedi.com")
    if request.method == 'POST':
        account = request.POST.get("account", None)
        password = request.POST.get("pass", None)
        a = (account + password)
        d = encode(a)
        password = db.query("Password,Department,Authority", "staffs", "Account", account)
        if d == password[0][0]:
            au = db.query("MissionCheck", "authority", "Authority", password[0][2])
            if au[0][0] == "仅自己":
                missions = db.query("*", "missions", "Executor", account)
                listMissions = []
                for i in range(len(missions)):
                    t = missions[i]
                    if t[12] == "已完成":
                        continue
                    v = dict([('from', "/Date(1320192000000)/"),
                              ('to', "/Date(1320592000000)/"),
                              ('label', ""),
                              ('customClass', "ganttRed")])
                    lv = []
                    lv.append(v)
                    showName = t[0]
                    if showName == "":
                        showName = t[2]
                    dictMissions = dict(name=showName, desc=t[5], values=lv)
                    listMissions.append(dictMissions)
                print(listMissions)
                ss = [{
                    'name': "task 请我 1",
                    'desc': "",
                    'values': [{
                        'from': "/Date(1320192000000)/",
                          'to': "/Date(1320592000000)/",
                        'label': "",
                        'customClass': "ganttRed"
                        }]
                    }, {
                    'name': "task 请我 2",
                    'desc': "",
                    'values': [{
                        'from': "/Date(1320192000000)/",
                          'to': "/Date(1320592000000)/",
                        'label': "",
                        'customClass': "ganttRed"
                        }]
                    }]
                print(type(ss))
                return render(request, "gantt.html", {'data': listMissions})
            else:
                return render(request, "ganttStaffs.html")
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")


def encode(s):
    b = bytes(s, encoding='gb2312')
    h = hashlib.sha512(b).digest()
    c = base64.b64encode(h)
    d = str(c, encoding='gb2312')
    return d
