from django.shortcuts import render
from missions import db
import hashlib
import base64
import json
# Create your views here.


def index(request):
    # data = db.query("Password", "staffs", "Account", "jinhe@smedi.com")
    if request.method == 'POST':
        account = request.POST.get("account", None)
        password = request.POST.get("pass", None)
        # print(account)
        # print(password)
        a = (account + password)
        d = encode(a)
        '''
        b = bytes(a, encoding='gb2312')
        h = hashlib.sha512(b).digest()
        c = base64.b64encode(h)
        d = str(c, encoding='gb2312')
        '''
        password = db.query("Password,Department,Authority", "staffs", "Account", account)
        print(password[0][0])
        print(d == password[0][0])
        if d == password[0][0]:
            au = db.query("MissionCheck", "authority", "Authority", password[0][2])
            if au[0][0] == "仅自己":
                missions = db.query("*", "missions", "Executor", account)
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
                jsonss = json.dumps(ss)
                print(type(ss))
                return render(request, "gantt.html", {'data': ss})
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
