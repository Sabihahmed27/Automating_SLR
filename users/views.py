from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from habanero import Crossref
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SimpleForm, QueryForm, DocumentForm
import requests,json
from django.http import JsonResponse
import urllib
import scholarly
from django.core import serializers
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

            print(type(content))

            context = {
                'form': form,
                'content': content
            }

            messages.success(request, f'Your Url has been generated')

            #return redirect(request,'users/query.html',{'content' : content})
            return render(request,'users/query.html', {'content': [content]})
            #return render(json.dumps(content,sort_keys=True, indent=4),'users/query.html', content_type="application/json"))
            #return (HttpResponse(json.dumps(content,sort_keys=True, indent=4), content_type="application/json"))


            # print(lists[0])

        #     form.save()

        else:
                messages.error(request,f'Wrong Url')
                return render(request, 'users/query.html', {'form': form})

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


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = DocumentForm()
    return render(request, 'users/model_form_upload.html', {'form': form})



def query(request):
    return render(request,'profile')


def scholarly_data(request):

    if request.method == 'POST':
        form2 = QueryForm(request.POST)

        if form2.is_valid():
            # query = input('Enter the query to be searched: ')
            query2 = form2.cleaned_data.get("query")
            #parameter_values_list = [1, 10, '9ipXPomYaSrHLAIuONZfzUGk3t57RcBD']
            #response = requests.get(edited_search_coreAPI(query, parameter_values_list))
            # response = requests.get(edited_search_coreAPI(form.enterUrl, parameter_values_list))
            #content = response.json()
            # print(content)
            #
            search_query = scholarly.search_author(query2)
            #print(next(search_query))
            #content = search_query.json()
            #lst = []


            for i in search_query:
                em_author = i.email
                auth_id = i.id
                auth_name = i.name
                print(i.name)

            context = {
                'form2': form2,
                'search_query': search_query,
                #'content': content
            }

            cr = Crossref()

            x = cr.works(query = 'Barbara  Ann Kitchenham',filter = {'has_full_text': True})
            print(len(x['message']['items']))
            lists_urls = x['message']['items']
            for i in x['message']['items']:
                print(i['link'])


            #dois = ['10.1186/s13643-018-0740-7']
            # x = cr.works(filter={"doi": ['10.1186/s13643-018-0740-7']})
            # # ,'has_full_text': True
            # for y in x['message']['items']:
            #     auth_URL = y['URL']
            #     print(y['URL'])
            # search_query = scholarly.search_pubs_query('guidelines for snowballing')
            # print(next(search_query))

            messages.success(request, f'Your Url has been generated')
            #return render_to_response(request, {"day_list": ['sunday', 'monday', 'tuesday']})
            # return redirect(request,'users/query.html',{'content' : content})
            return render(request, 'users/scholar.html', {'content': [search_query]})
            #return render(request, 'users/query.html',{"content" : content})
            #return render(json.dumps(search_query,sort_keys=True, indent=4),'users/query.html', content_type="application/json")
            #query_serialized = serializers.serialize('json', search_query)
            #return JsonResponse(query_serialized, safe=False)
            #return (HttpResponse(json.dumps(search_query,sort_keys=True, indent=4), content_type="application/json"))
            #return render(request, 'users/scholar.html', {"data": data, "country_list": country_list})

        #return (HttpResponse((search_query), content_type="application/json"))

        else:
            messages.error(request, f'Wrong Url')
            return render(request, 'users/scholar.html', {'form2': form2})

    else:
        form2 = QueryForm()
        return render(request, 'users/scholar.html', {'form2': form2})











