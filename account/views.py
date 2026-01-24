from django.shortcuts import render ,redirect
from .forms import SignUpForm,LoginForm,SignUpEditForm,UpdateUserForm
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth import get_user_model
from account.models import User
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404

def login_request(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.status == 'active':
                messages.success(request, 'Giriş Başarılı.')
                if user.authorization == "3":
                    return redirect('repair_orders')
                else:
                    return redirect('home')
            else:
                messages.info(request, "Kullanıcı 'Pasif' durumda, yönetici ile iletişime geçiniz.")
        else:
            messages.warning(request, "Kullanıcı adı veya parola yanlış.")
    return render(request, "page/login.html", context={'form': form})

def logout_request(request):
    messages.add_message(
                request,messages.WARNING,
                        f"*{request.user.username}* Kullanıcısı için oturum kapatıldı." )
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@administrator
def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            messages.add_message(
                request,messages.SUCCESS,
                        f"*{user.username}* Kullanıcısı kaydedildi." )
            return redirect ('users_home')
        else:
            messages.add_message(
            request,messages.WARNING,
            form.errors.as_ul())
    else:
        form = SignUpForm()
    return render(request,"page/register.html",context={'form':form})

@login_required(login_url="login")
@administrator
def users_home(request):
    context = dict()
    context["users"]= get_user_model().objects.all()
    return render(request ,'page/login_home.html',context)

@login_required(login_url="login")
@administrator
def userDelete(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('id'))
        if user.is_superuser:
            messages.add_message(
            request,messages.WARNING,
            f'*{user.username}* kullanıcısı Yönetici olduğundan silinemez.')
        else:
            try:
                user.delete()
                messages.add_message(
                request,messages.SUCCESS,
                f'*{user.username}* kullanıcısı silindi.')
            except ProtectedError:
                messages.add_message(
                                request,messages.WARNING,
                                f'*{ user.username }* Kullanıcı diğer tablolarda kullanılmakta.Kullanıcı kaydını silmek için diğer tablolardan kayıtlı verileri silmelisiniz.!Kullanıcıyı *PASİF* duruma getirebilirsiniz.' )
    return redirect('users_home')

@login_required(login_url="login")
@administrator
def updateUser(request, myid):
    user = get_object_or_404(User, id=myid)
    if request.method == "POST":
        form = SignUpEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if user.is_superuser and form.cleaned_data["status"] == "passive":
                messages.warning(request, f'*{user.username}* kullanıcısı Yönetici olduğundan PASİF duruma getirilemez.')
                return redirect('users_home')
            else:
                user = form.save()
                messages.success(request, f'*{user.username}* kullanıcısına ait bilgiler güncellendi.')
                return redirect('users_home')
        else:
            messages.warning(
            request,
            f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}")
    else:
        form = SignUpEditForm(instance=user)
    return render(request, "page/register_edit.html", context={'form': form, 'sel_item': user})

@login_required(login_url="login")
@administrator
def update_password(request, myid):
    user = get_object_or_404(User, username=myid)
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, f'*{user.username}* Kullanıcısı için şifre güncellendi.')
                return redirect('users_home')
            else:
                messages.warning(request, "Şifreler uyuşmuyor.")
        else:
            messages.warning(request, form.errors.as_text())
    return render(request, "page/update_password.html")
