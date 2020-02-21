from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from sqlitedict import SqliteDict
from django.urls import reverse
from habanero import Crossref
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SimpleForm, QueryForm, DocumentForm
import requests,json
from django.http import JsonResponse
import urllib
from urllib.error import HTTPError
from crossref.restful import Works
import scholarly
import re
from django.core import serializers
from urllib.parse import urlencode, quote_plus,quote


common_dois = []


# Create your views here.
class paper_details:
    def __init__(self,doi,title,year,url):
        self.title = title
        self.doi = doi
        self.year = year
        self.url = url




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

def review(request):
    return render(request,'users/review.html')

def data(request):

    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            #query = input('Enter the query to be searched: ')
            query = form.cleaned_data.get("Title")

            parameter_values_list = [1, 100, '9ipXPomYaSrHLAIuONZfzUGk3t57RcBD']
            response = requests.get(edited_search_coreAPI(query, parameter_values_list))
            try:

                content = response.json()
                core_doi_list = []
                crossref_doi_list = []
                crossref_class_list = []

                cr = Crossref()


                if not str(query).isalnum():
                    query = re.sub(r"[^a-zA-Z0-9]+", ' ', query)

                    query = re.sub(' +', ' ', query)

                if len(query.replace(" ","")) == 0:
                    temp_messages = 'Invalid Input! Please provide a valid input'
                    # messages.error(request, f'Wrong Url')
                    return render(request, 'users/scholar.html', {'form': form, 'temp_messages':temp_messages})

                # if query.isa
                #     return render(request, 'users/scholar.html', {'form': form})


                x = cr.works(query=query, filter={'has_full_text': True})
                if x['status'] == "error":
                    return render(request, 'users/scholar.html', {'form': form})




                crossref_titles = []
                crossref_year = []
                crossref_url = []


                for i in x['message']['items']:
                    crossref_titles.append(str(i['title'][0]))
                    crossref_year.append(i['created']['date-parts'][0][0])
                    crossref_url.append(i['URL'])
                    crossref_doi_list.append(i['DOI'])
                    # print(i['DOI'])
                    # temp_doi = i['DOI']
                    # temp_title = i['title']
                    # temp_year = i['created']['date-parts'][0][0]
                    # temp_url = i['URL']
                    # crossref_class_list.append(paper_details(temp_doi,temp_title,temp_year,temp_url))


                core_class_list = []




                core_title = []
                core_url = []
                core_year = []
                if content.__contains__('data'):
                    if content['data'] is not None:
                        for i in content['data']:
                            if i['_source'].__contains__('doi'):
                                if i['_source']['doi'] is not None:
                                    # print(str(i['_source']['title']) + " "+str(i['_source']['datePublished']))
                                    core_doi_list.append(i['_source']['doi'])
                                    core_year.append(i['_source']['datePublished'])
                                    core_title.append(i['_source']['title'])
                                    if len(i['_source']['urls']) > 0:
                                        core_url.append(i['_source']['urls'][0])
                                        # print(i['_source']['urls'][0])
                                    else:
                                        core_url.append(None)
                                    # print(i['_source']['doi'])
                # else:
                #     return render(request, 'users/scholar.html', {'form': form})


                # print("Before duplication")
                # print(len(crossref_titles))
                # print(len(core_title))
                new_core_title = []
                for i in core_title:
                    if i not in new_core_title:
                        new_core_title.append(i)
                # print("After deduplication")
                # print(len(new_core_title))



                new_crossref_year = []
                for i in crossref_year:
                    if i not in new_crossref_year:
                        new_crossref_year.append(i)



                new_crossref_url = []
                for i in crossref_url:
                    if i not in new_crossref_url:
                        new_crossref_url.append(i)








                new_crossref_titles=[]
                for i in crossref_titles:
                    if i not in new_crossref_titles:
                        new_crossref_titles.append(i)


                new_core_title = []
                for i in core_title:
                    if i not in new_core_title:
                        new_core_title.append(i)

                # print("Length of titles")

                # print(len(new_core_title))
                # print("After deduplication")
                # print(len(new_core_title))



                new_core_year = []
                for i in core_year:
                    if i not in new_core_year:
                        new_core_year.append(i)

                # print("Length of years")
                #
                # print(len(new_core_year))
                #



                new_core_url = []
                for i in core_url:
                    if i not in new_core_url:
                        new_core_url.append(i)
                # print("Length of urls")
                #
                # print(len(new_core_url))




                # print("After de duplication")
                # print(len(new_crossref_titles))
                # for i in new_crossref_titles:
                #     print(i)
                #

                # common_dois = []
                common_title = []
                # common_title = list(set(new_crossref_titles) & set(new_core_title))
                # print(len(common_title))

                # common_dois = list(set(crossref_doi_list) & set(core_doi_list))
                # print(len(common_dois))
                # for i in common_dois:
                    # print(i)


                context = {
                    # 'form': form,
                    # 'content': content,
                    'crossref_dois' : crossref_doi_list,
                    'core_doi_list': core_doi_list,
                    'crossref_class_list': crossref_class_list,
                    'core_class_list':core_class_list


                }
                crossref_dup = zip(crossref_titles,crossref_year,crossref_url)
                crossRef = zip(new_crossref_titles,new_crossref_year,new_crossref_url)

                core_dup = zip(core_title,core_year,core_url)
                core = zip(new_core_title,new_core_year,new_core_url)

                messages.success(request, f'Your Database has been successfully retrieved')

                database = SqliteDict('./database.sqlite',autocommit=True)
                print(database['snowballing'])
                common_dois = core_doi_list
                common_dois.extend(crossref_doi_list)
                request.session['list'] = common_dois

                # return redirect("query", data=str(common_dois))


            # return render(request, 'users/query.html',data=str(content))
                return render(request, 'users/scholar.html', {'crossref_dois': crossref_doi_list,
                                                              'core_doi_list': core_doi_list,
                                                              'new_crossref_titles' : new_crossref_titles,
                                                              'crossref_year': crossref_year,
                                                              'crossRef': crossRef,
                                                              'coredup':core_dup,
                                                              'core':core,
                                                              'crossref_dup':crossref_dup,
                                                              'crossref_url':crossref_url,

                                                              'new_core_title':new_core_title,
                                                              'core_year':core_year,
                                                              'core_url':core_url,
                                                              'form': form

                                                              })
            except HTTPError:
                messages.error(request,f'No response from Server')
                return render(request, 'users/scholar.html', {'form': form})


        else:
                #messages.error(request,f'Wrong Url')
                return render(request, 'users/scholar.html', {'form': form})

    else:
        form = SimpleForm()
        return render(request, 'users/scholar.html', {'form': form})
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
def funct():
    return common_dois

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

    return render(request,'users/query.html',{data:data})


def snowballing(request):
    print("Snowballing dois")

    com = request.session['list']

    for i in com:
        print(i)

    database = SqliteDict('./database.sqlite', autocommit=True)
    dois = []

    for i in com:

        if i in database['snowballing']:

            dois.append(database['snowballing'][i])


    return render(request,'users/snowballing.html',{'com': dois})


def scholarly_data(request):

    if request.method == 'POST':
        form2 = QueryForm(request.POST)

        if form2.is_valid():
            # query = input('Enter the query to be searched: ')
            query2 = form2.cleaned_data.get("enterUrl")
            #parameter_values_list = [1, 10, '9ipXPomYaSrHLAIuONZfzUGk3t57RcBD']
            #response = requests.get(edited_search_coreAPI(query, parameter_values_list))
            # response = requests.get(edited_search_coreAPI(form.enterUrl, parameter_values_list))
            #content = response.json()
            # print(content)
            #
            search_query = scholarly.search_keyword(query2)
            #print(next(search_query))
            #content = search_query.json()
            #lst = []


            for i in search_query:
                em_author = i.email
                auth_id = i.id
                auth_name = i.name
                print(i.name)



            cr = Crossref()

            x = cr.works(query = query2,filter = {'has_full_text': True})
            print(len(x['message']['items']))
            url_list = []
            crossref_list = []
            lists_urls = x['message']['items']
            # for i in x['message']['items']:
            #     crossref_list.append(paper_details(i['doi'], i['title']))
                #url_list.append(i['link'][0]['URL'])

            # for i in crossref_list:
            #     if()
            temp =[]
            for i in x['message']['items']:
                temp.append(i['title'])
            temp_urls = []

            for i in x['message']['items']:
                temp_urls.append(i['URL'])

            context = {
                'form2': form2,
                'search_query': search_query,
                #'content': content
            }




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
            zip_lists = list(zip(temp,temp_urls))
            return render(request, 'users/database.html', {'content': zip_lists})
            #return render(request, 'users/query.html',{"content" : content})
            #return render(json.dumps(search_query,sort_keys=True, indent=4),'users/query.html', content_type="application/json")
            #query_serialized = serializers.serialize('json', search_query)
            #return JsonResponse(query_serialized, safe=False)
            #return (HttpResponse(json.dumps(search_query,sort_keys=True, indent=4), content_type="application/json"))
            #return render(request, 'users/scholar.html', {"data": data, "country_list": country_list})

        #return (HttpResponse((search_query), content_type="application/json"))

        else:
            #messages.error(request, f'Wrong Url')
            return render(request, 'users/database.html', {'form2': form2})

    else:
        form2 = QueryForm()
        return render(request, 'users/database.html', {'form2': form2})











