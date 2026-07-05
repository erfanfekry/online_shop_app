import random
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.sms_verification.sms_verification import *
from .forms import *


class UserLogin(LoginView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'registration/login.html')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'action_button' in request.POST:
            if request.POST.get('action_button') == 'Yes':
                logout(request)
                return redirect('account:login')
            else:
                return redirect('shop:product-list')
        return super().post(request, *args, **kwargs)


@login_required
def user_logout(request):
    if request.method == 'POST':
        print('POST: ', request.POST.get('action_button'))
        if request.POST.get('action_button') == 'Yes':
            messages.success(request, 'You\'re logged out')
            logout(request)
            return redirect('account:login')
        else:
            return redirect('shop:product-list')
    return render(request, 'registration/logout.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password'])
            user.save()
            return render(request, 'registration/user_register-done.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/user_register.html', {'form': form})


@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'registration/user_edit-done.html', {'form': form})
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'registration/user_register.html', {'form': form})



def phone_verification(request):
    if request.user.is_authenticated:
        return redirect('order:make-order')
    else:
        if request.method == 'POST':
            form = PhoneVerificationForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data.get('phone')
                verification_code = ''.join(random.choices('123456789', k=6))
                # verification_sms(number=int(phone),
                #                  template_id=130765,
                #                  parameters=[{'name': 'FULLNAME', 'value': f'{request.user.first_name}'},
                #                               {'name': 'CODE', 'value': f'{verification_code}'}])
                print('verify code: ', verification_code)
                request.session['verification_code'] = verification_code
                request.session['phone'] = phone
                messages.success(request, f'یک پیامک حاوی کد تایید برای شماره {phone} ارسال گردید.')
                return redirect('account:code-confirm')
        else:
            form = PhoneVerificationForm()
        return render(request, 'verification/phone_verification.html', {'form': form})


def code_confirm(request):
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if request.session.get('verification_code') != cd.get('verification_code'):
                messages.error(request, 'کد وارد شده صحیح نیست!')
            else:
                phone = request.session.get('phone')
                if ShopUser.objects.filter(phone=phone).exists():
                    user = ShopUser.objects.get(phone=phone)
                else:
                    user = ShopUser.objects.create(phone=phone)
                    user.set_password('123456')
                    user.save()
                    message = (f'کاربر گرامی : مریم موشی '
                               '\n'
                               f'یک حساب کاربری با مشخصات زیر برای شما ساخته شد:'
                               '\n'
                               f'نام کاربری: چاقا '
                               '\n'
                               f'رمز عبور: {123456}'
                               '\n'
                               f'گروه آموزشی لاگام')

                    notification_sms(number=phone, message=message)
                    print(message)

                cart = request.session.get('cart')
                login(request, user)
                request.session['cart'] = cart
                del request.session['phone']
                del request.session['verification_code']
                return redirect('order:make-order')

    else:
        form = CodeVerificationForm()
    return render(request, 'verification/confirm_code.html', {'form': form})
