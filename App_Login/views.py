from django.shortcuts import render, HttpResponseRedirect
from App_Login.forms import CreateNewUser, EditProfile
from django.contrib.auth import authenticate, login, logout  
from django.urls import reverse, reverse_lazy
from App_Login.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from App_Login.models import AdminUser
from .forms import PlanForm
from core.models import Plan,Subscription,ExchangeRateLog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import AdminUser


def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            
            return HttpResponseRedirect(reverse('App_Login:login' ))  

    return render(request, 'App_Login/signup.html', context={'title': 'Signup Form Here', 'form': form})  

  

from App_Login.models import AdminUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from decimal import Decimal

def login_page(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            
            user = form.get_user()
            login(request, user)
            return redirect('App_Login:index')

       
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = AdminUser.objects.get(username=username)
            if admin.password1 == password:
                request.session['admin_username'] = admin.username
                return redirect('App_Login:dashboard')
        except AdminUser.DoesNotExist:
            pass  

        form.add_error(None, "Invalid username or password.")

    return render(request, 'App_Login/login.html', {'form': form})
@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance = current_user)
    return render(request, 'App_Login/profile.html',context = {'title':'Edit Profile Page','form': form})    
    

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


from datetime import datetime, timedelta

from django.contrib.auth.models import User
@login_required
def index(request):
    # if not request.session.get('admin_username'):
    #     return redirect('App_Login:login')
    if not request.user.is_authenticated and not request.session.get('admin_username'):
        return redirect('App_Login:login')
    plans = Plan.objects.all()
    subscriptions = Subscription.objects.select_related('user', 'plan')
    exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

    if request.method == 'POST':
        action = request.POST.get('action')
        plan_id = request.POST.get('plan_id')
        user_id = request.POST.get('user_id')

        if action == 'activate':
            plan = Plan.objects.get(id=plan_id)
            user = User.objects.get(id=user_id)
            start_date = datetime.now()
            end_date = start_date + timedelta(days=plan.duration_days)

            
            Subscription.objects.filter(user=user, status='active').update(status='cancelled')

            Subscription.objects.create(
                user=user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                status='active'
            )
            return redirect('App_Login:index')

        elif action == 'cancel':
            sub_id = request.POST.get('subscription_id')
            sub = Subscription.objects.get(id=sub_id)
            sub.status = 'cancelled'
            sub.save()
            return redirect('App_Login:index')

    
    for sub in subscriptions:
        if sub.status == 'active' and sub.end_date < datetime.now().date():
            sub.status = 'expired'
            sub.save()

    
    enriched_rates = []
    for rate in exchange_rates:
        converted = []
        for plan in plans:
            converted_price = round(Decimal(plan.price) * Decimal(rate.rate), 2)
            converted.append({
                'plan_name': plan.name,
                'usd_price': plan.price,
                'converted_price': converted_price,
            })
        enriched_rates.append({
            'base': rate.base_currency,
            'target': rate.target_currency,
            'rate': rate.rate,
            'fetched_at': rate.fetched_at,
            'plans_converted': converted
        })

    return render(request, 'App_Login/index.html', {
        'title': 'User Dashboard',
        'plans': plans,
        'subscriptions': subscriptions,
        'exchange_rates': enriched_rates,
        'plan_form': PlanForm(),
        'users': User.objects.all(),  
    })
def dashboard(request):
    if request.session.get('admin_username'):
        return render(request, 'App_Login/dashboard.html', {'title': 'Admin Dashboard'})
    else:
        return HttpResponseRedirect(reverse('App_Login:login'))
def dashboard(request):
    if not request.session.get('admin_username'):
        return redirect('App_Login:login')

    plans = Plan.objects.all()
    subscriptions = Subscription.objects.select_related('user', 'plan')
    exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

    
    plan_form = PlanForm()
    if request.method == 'POST':
        plan_form = PlanForm(request.POST)
        if plan_form.is_valid():
            plan_form.save()
            return redirect('App_Login:dashboard')  

    return render(request, 'App_Login/dashboard.html', {
        'title': 'Admin Dashboard',
        'plans': plans,
        'subscriptions': subscriptions,
        'exchange_rates': exchange_rates,
        'plan_form': plan_form
    })
from decimal import Decimal

def dashboard(request):
    if not request.session.get('admin_username'):
        return redirect('App_Login:login')

    plans = Plan.objects.all()
    subscriptions = Subscription.objects.select_related('user', 'plan')
    exchange_rates = ExchangeRateLog.objects.order_by('-fetched_at')[:10]

    
    plan_form = PlanForm()
    if request.method == 'POST':
        plan_form = PlanForm(request.POST)
        if plan_form.is_valid():
            plan_form.save()
            return redirect('App_Login:dashboard')

    
    enriched_rates = []
    for rate in exchange_rates:
        converted = []
        for plan in plans:
            converted_price = round(Decimal(plan.price) * Decimal(rate.rate), 2)
            converted.append({
                'plan_name': plan.name,
                'usd_price': plan.price,
                'converted_price': converted_price,
            })
        enriched_rates.append({
            'base': rate.base_currency,
            'target': rate.target_currency,
            'rate': rate.rate,
            'fetched_at': rate.fetched_at,
            'plans_converted': converted
        })

    return render(request, 'App_Login/dashboard.html', {
        'title': 'Admin Dashboard',
        'plans': plans,
        'subscriptions': subscriptions,
        'exchange_rates': enriched_rates,
        'plan_form': plan_form,
    })
