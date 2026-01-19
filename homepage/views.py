from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import *

@login_required(login_url="login")
@administrator
def index(request):
    return render(request,"index.html")