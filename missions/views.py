from django.shortcuts import render
from missions import db

# Create your views here.


def index(request):
    data = db.query("testtable")
    return render(request, "index.html")

