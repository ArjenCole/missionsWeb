from django.shortcuts import render
from missions import db
import hashlib
import base64
import time
import datetime
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
        dictMissions = getdict(t)
        listMissions.append(dictMissions)
    return listMissions


def getdict(t):
    lv = getValues(t)
    showName = t[0]
    if showName == "":
        showName = t[2]
    return dict(name=showName, desc=t[5], values=lv)


def getValues(t):
    v = dict([('from', timeFormat(timeDiffer(t[9]))),
              ('to', timeFormat(timeDiffer(t[10]))),
              ('label', ""),
              ('customClass', "ganttRed")])
    lv = []
    lv.append(v)
    return lv


def timeDiffer(date1, date2="1970-1-1"):
    date1Replace = date1.replace("/", "-") + " 00:00:00"
    date2Replace = date2.replace("/", "-") + " 00:00:00"
    if str(date1Replace) == " 00:00:00":
        date1Replace = "1970-1-1 00:00:00"
        print("e1" + date1Replace + "dd")
    if str(date2Replace) == " 00:00:00":
        date2Replace = "1970-1-1 00:00:00"
    date1 = time.strptime(date1Replace, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2Replace, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    return (date1-date2).days


def timeFormat(days):
    return "/Date(" + str(days * 86400000) + ")/"

