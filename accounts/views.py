from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm 
from django.contrib.auth import authenticate, login, logout
from accounts.forms import EditUserProfileForm, ProfilePicForm
from django.contrib.auth.decorators import login_required
# Create your views here.


# user register views
def register_view(request):
    context = {}
    form = UserRegistrationForm()
    if request.method == 'POST':
        agree = request.POST.get('consent')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            ###### code for automatic login after registration if user check the Keep Login Me #######     
            if agree == 'YES':
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, 'Loged in successfully ' + username)
                # return redirect('account_settings')
            else:
                messages.success(request, 'Account Created successfully ' + username)
                return redirect('accounts:login')

    context['form'] = form
    return render(request, 'accounts/register.html', context)



# User Login views
def login_view(request):
    context ={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, 'Logged in successfully ' + username)
                return redirect('home:home_page')
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'accounts/login.html', context)


# User Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'Loged out successfully!')
    return redirect('home:home_page')



# User Account settings view
@login_required(login_url='accounts:login')
def account_settigs_view(request):
    context = {}
    if request.method == 'POST':
        u_form = EditUserProfileForm(request.POST, instance=request.user)
        p_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profilepic)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, 'Your profile is updated successfully!')
            u_form.save()
            p_form.save()
    else:
        u_form = EditUserProfileForm(instance=request.user)
        p_form = ProfilePicForm(instance=request.user.profilepic)
    context['u_form'] = u_form
    context['p_form'] = p_form
    return render(request, 'accounts/account_settings.html', context)
