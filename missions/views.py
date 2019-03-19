from django.shortcuts import render
from missions import db
import hashlib

# Create your views here.


def index(request):
    # data = db.query("Password", "staffs", "Account", "jinhe@smedi.com")

    if request.method == 'POST':
        account = request.POST.get("account", None)
        password = request.POST.get("pass", None)
        print(account)
        print(password)
        a = (account + password)
        b = a.encode(encoding='gb2312', errors = 'strict')
        print(b)
        print(hashlib.sha512(b).hexdigest())
        return render(request, "gantt.html")
    else:
        return render(request, "index.html")


