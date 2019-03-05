from django.shortcuts import render
from missions import db

# Create your views here.


def index(request):
    # data = db.query("testtable")
    if request.method == 'POST':
        return render(request, "gantt.html")
    else:
        return render(request, "index.html")


