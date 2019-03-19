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
        password = db.query("Password", "staffs", "Account", account)
        print(password[0][0])
        print(d == password[0][0])
        if d == password[0][0]:
            return render(request, "gantt.html")
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
