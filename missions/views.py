from django.shortcuts import render
from missions import db
import hashlib
import base64
# Create your views here.


def index(request):
    if request.method == 'POST':
        account = request.POST.get("account", None)
        authority = login(request.POST)
        if authority != "登陆失败":
            mc = db.query("MissionCheck", "authority", "Authority", authority)
            if mc[0][0] == "仅自己":
                listMissions = getMissons(account)
                return render(request, "gantt.html", {'data': listMissions})
            else:
                return render(request, "ganttStaffs.html")
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")


def login(post):
    account = post.get("account", None)
    password = post.get("pass", None)
    a = (account + password)
    d = encode(a)
    password = db.query("Password,Department,Authority", "staffs", "Account", account)
    if d == password[0][0]:
        return password[0][2]
    else:
        return "登陆失败"


def encode(s):
    b = bytes(s, encoding='gb2312')
    h = hashlib.sha512(b).digest()
    c = base64.b64encode(h)
    d = str(c, encoding='gb2312')
    return d


def getMissons(account):
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
    return listMissions
