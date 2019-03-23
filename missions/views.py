from django.shortcuts import render
from missions import db
import hashlib
import base64
import time
import datetime
import json
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
                listMissions = getMissons(account)
                return render(request, "gantt.html", {'data': listMissions})
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
    # data = json.dumps(t, ensure_ascii=False)
    data = {'name': t[0], 'project_Index': t[1], 'project_Name': t[2],
            'project_Location': t[3], 'project_Stage': t[4],
            'schedule': t[5], 'majorDepartment': t[6], 'major': t[7],
            'version': t[8],
            'date_Handover': t[9], 'date_Submit': t[10], 'date_Publish': t[11],
            'status': t[12],
            'project_Manager': t[13], 'technical_Director': t[14], 'designer': t[15],
            'proofreader': t[16], 'auditor': t[17], 'executor': t[18],
            'expDays': t[19], 'remark': t[20], 'key': t[21], 'date_Finish': t[22],
            'workCost': t[23], 'fee': t[24], 'date_Create': t[25], 'creator': t[26]}
    data = json.dumps(data, ensure_ascii=False)
    v = dict([('from', timeFormat(timeDiffer(t[9]))),
              ('to', timeFormat(timeDiffer(t[10]))),
              # ('desc', "123"),
              ('label', t[4]),
              ('dataObj', data),
              ('customClass', getGanttColor(timeDiffer(t[10], t[9]), t[4]))])
    lv = []
    lv.append(v)
    return lv


def getGanttColor(days, stage):
    ganttColor = "ganttGreen"
    if stage == "施设":
        if days < 2:
            ganttColor = "ganttBlue"
        elif days < 4:
            ganttColor = "ganttRed"
        elif days < 6:
            ganttColor = "ganttOrange"
        else:
            ganttColor = "ganttGreen"
    elif stage == "初设":
        if days < 1:
            ganttColor = "ganttBlue"
        elif days < 3:
            ganttColor = "ganttRed"
        elif days < 5:
            ganttColor = "ganttOrange"
        else:
            ganttColor = "ganttGreen"
    else:
        if days < 1:
            ganttColor = "ganttRed"
        elif days < 2:
            ganttColor = "ganttOrange"
        else:
            ganttColor = "ganttGreen"
    return ganttColor


def timeDiffer(date1, date2="1970-1-1"):
    date1Replace = date1.replace("/", "-") + " 00:00:00"
    date2Replace = date2.replace("/", "-") + " 00:00:00"
    if str(date1Replace) == " 00:00:00":
        date1Replace = str(datetime.date.today()) + " 00:00:00"
    if str(date2Replace) == " 00:00:00":
        date2Replace = str(datetime.date.today()) + " 00:00:00"
    date1 = time.strptime(date1Replace, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2Replace, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    return (date1-date2).days


def timeFormat(days):
    return "/Date(" + str(days * 86400000) + ")/"

