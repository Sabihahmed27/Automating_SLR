from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SimpleForm
import requests,json
import urllib
from urllib.parse import urlencode, quote_plus,quote


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to Login')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'users/profile.html',context)


def data(request):

    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            #query = input('Enter the query to be searched: ')
            query = form.cleaned_data.get("enterUrl")
            parameter_values_list = [1, 10, '9ipXPomYaSrHLAIuONZfzUGk3t57RcBD']
            response = requests.get(edited_search_coreAPI(query, parameter_values_list))
            # response = requests.get(edited_search_coreAPI(form.enterUrl, parameter_values_list))
            content = response.json()
            print(content)

            context = {
                'form': form,
                'content': content
            }

            messages.success(request, f'Your Url has been generated')
            #return render(response, 'users/query.html', {'form': context})
            #return render(json.dumps(content,sort_keys=True, indent=4),'users/query.html', content_type="application/json"))
            return (HttpResponse(json.dumps(content,sort_keys=True, indent=4), content_type="application/json"))


            # print(lists[0])

        #     form.save()

        else:
                messages.error(request,f'Wrong Url')
                return render(request, 'users/data.html', {'form': form})

    else:
        form = SimpleForm()
        return render(request, 'users/data.html', {'form': form})
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your Url has been generated')
    #         #return redirect('register')
    #
    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)
    #


def edited_search_coreAPI(query, parameter_values_list):
    url = 'https://core.ac.uk:443/api-v2/search/'
    url += quote(query)

    parameter_list = ['page', 'pageSize', 'apiKey']

    parameters = {}

    for i in range(len(parameter_list)):
        key = parameter_list[i]
        value = parameter_values_list[i]
        parameters[key] = value

    # print("{}?{}".format(url, urllib.parse.urlencode(parameters)))
    url = "{}?{}".format(url, urllib.parse.urlencode(parameters))
    return url



