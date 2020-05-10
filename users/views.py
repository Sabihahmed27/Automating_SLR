from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from sqlitedict import SqliteDict
from django.urls import reverse
from habanero import Crossref
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from .models import Document, Snowballing_model
from users.models import Articles
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SimpleForm, QueryForm, DocumentForm, \
    AbstractForm, PICOC
import requests,json
from django.http import JsonResponse
import urllib
from urllib.error import HTTPError
#from Crossref.restful import Works
from django.db.models import Q
import scholarly
import re
from django.core import serializers
from urllib.parse import urlencode, quote_plus,quote
from whoosh import index,query as q,qparser
#from whoosh.lang.morph_en import variations

#import whoosh
from whoosh.fields import Schema , TEXT, ID
from whoosh.analysis import StemmingAnalyzer

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

@login_required()
def data(request):

    if request.method == 'POST':
        form = SimpleForm(request.POST)
        form2 = PICOC(request.POST)

        if form.is_valid() and form2.is_valid():
            #query = input('Enter the query to be searched: ')
            query = form.cleaned_data.get("Title")
            startYear = form.cleaned_data.get("StartYear")
            endYear = form.cleaned_data.get("EndYear")
            author = form.cleaned_data.get("Author")
            keyword = form.cleaned_data.get("Keyword")


            population = form2.cleaned_data.get("population")
            intervention = form2.cleaned_data.get("intervention")
            comparison = form2.cleaned_data.get("comparison")
            outcome = form2.cleaned_data.get("outcome")
            context = form2.cleaned_data.get("context")





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

                if not str(author).isalnum():
                    query = re.sub(r"[^a-zA-Z0-9]+", ' ', query)

                    query = re.sub(' +', ' ', query)

                if len(author.replace(" ","")) == 0:
                    temp_messages = 'Invalid Input! Please provide a valid Author name'
                    # messages.error(request, f'Wrong Url')
                    return render(request, 'users/scholar.html', {'form': form, 'temp_messages':temp_messages})

                if len(query.replace(" ","")) == 0:
                    temp_messages = 'Invalid Input! Please provide a valid Title'
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

                for i in set(new_core_title).union(set(new_crossref_titles)):
                    a = Articles(Title=i)
                    a.save()

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

                common_dois = core_doi_list
                common_dois.extend(crossref_doi_list)
                request.session['list'] = common_dois
                request.session['StartYear'] = startYear
                request.session['EndYear'] = endYear
                request.session['author'] = author
                request.session['Keyword'] = keyword

                core_heading = 'Results from Core'
                crossref_heading = 'Results from Crossref'

                # return redirect("query", data=str(common_dois))
                #removed some elements to be sent to html: new_crossref_titles,crossref_year,crossref_url,new_core_title, core_year, core_url


            # return render(request, 'users/query.html',data=str(content))
                return render(request, 'users/scholar.html', {'crossref_dois': crossref_doi_list,
                                                              'core_doi_list': core_doi_list,
                                                              'crossRef': crossRef,
                                                              'core_heading':core_heading,
                                                              'crossref_heading':crossref_heading,
                                                              'core':core,
                                                              'form': form,
                                                              'form2':form2
                                                              })
            except HTTPError:
                messages.error(request,f'No response from Server')
                return render(request, 'users/scholar.html', {'form': form})


        else:
                #messages.error(request,f'Wrong Url')
                return render(request, 'users/scholar.html', {'form': form})

    else:
        form = SimpleForm()
        form2 = PICOC()
        return render(request, 'users/scholar.html', {'form': form,'form2':form2})
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


def filter_articles(articles_list, starting_year, ending_year, input_author_list, article_info_db):
    result = set()

    if articles_list:

        for j in articles_list:

            if article_info_db.__contains__(j):

                if j and len(article_info_db[j]['year']) > 0 and len(article_info_db[j]['author']) > 0:

                    author_list = article_info_db[j]['author']

                    final_list_author = re.split(',|;| ', author_list)

                    final_list = [i for i in final_list_author if i]

                    if ending_year >= int(article_info_db[j]['year']) >= starting_year or len(
                            set(final_list).intersection(set(input_author_list))) > 0:
                        result.add(j)

                if j and (not article_info_db[j]['year'] or not article_info_db[j]['author']):
                    result.add(j)

    doi_map = {}
    for i in result:
        doi_map[i] = article_info_db[i]['title']
        # s = Snowballing_model(Title = article_info_db[i]['title'])
        # s.save()






    return doi_map


final_result = {}

final_result['references']={}

final_result['citations']={}


# final_result['references']['doi'] = {}
#
# final_result['references']['title'] = {}
#
# final_result['citations']['doi'] = {}
#
# final_result['citations']['title'] = {}

# class SearchResultsView(ListView):
#     model = City
#     template_name = 'search_results.html'
#
#     def get_queryset(self): # new
#         query = self.request.GET.get('q')
#         object_list = City.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
#         return object_list

def perform_snowballing(doi_list, starting_year, ending_year, authors, snowball_type, iteration):
    database = SqliteDict('./SLR_database.sqlite', autocommit=True)

    database_snowballing = database['snowballing']
    if iteration > 2:

        return

    else:

        for i in doi_list:

            if database_snowballing.__contains__(i):

                type_articles = database_snowballing[i][snowball_type]



                snowball_result = filter_articles(type_articles, starting_year, ending_year, authors, database_snowballing)

                if snowball_result:
                    doi_list = snowball_result.keys()



                    final_result[snowball_type].update(snowball_result)

            # print(doi_list)

        perform_snowballing(doi_list, starting_year, ending_year, authors, snowball_type,
                            iteration + 1)


# database = SqliteDict('./SLR_database.sqlite', autocommit=True)
#
# database_snowballing = database['snowballing']
#
# starting_year = 2010
#
# ending_year = 2018
#
# authors = ['Kitchenham', 'Barbara']
#
# doi_list_initial = ['10.2903/sp.efsa.2018.EN-1427', '10.5277/e-Inf180104', '10.1145/2745802.2745818',
#                     '10.1145/2601248.2601268', '10.1016/j.infsof.2010.03.006', '10.1186/s13643-018-0740-7']
#
# examined_articles = []
#
# perform_snowballing(doi_list_initial, starting_year, ending_year, authors, database_snowballing, 'citations', 0)
#
# perform_snowballing(doi_list_initial, starting_year, ending_year, authors, database_snowballing, 'references', 0)
#
# print("Backward: " + str(len(final_result['references'])))
# print("Forward: " + str(len(final_result['citations'])))



def query(request):

    return render(request,'users/query.html',{data:data})

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def snowballing(request):

    database = SqliteDict('./SLR_database.sqlite', autocommit=True)

    database_snowballing = database['snowballing']

    starting_year = 2010

    ending_year = 2018
    authors = []
    if request.session['author']:
        authors = request.session.get('author').split(' ')
    # else:
    #     authors  = ['Kitchenham', 'Barbara']

    if request.session['StartYear']:
        starting_year = request.session.get('StartYear')


    if request.session['EndYear']:
        ending_year = request.session.get('EndYear')

    print("Start Year " + str(starting_year))
    print("Ending Year " + str(ending_year))
    print("Author " + str(authors))





    doi_list_initial =  request.session['list']

    # doi_list_initial = ['10.2903/sp.efsa.2018.EN-1427', '10.5277/e-Inf180104', '10.1145/2745802.2745818',
    #                     '10.1145/2601248.2601268', '10.1016/j.infsof.2010.03.006', '10.1186/s13643-018-0740-7']

    examined_articles = []

    perform_snowballing(doi_list_initial, starting_year, ending_year, authors, 'citations', 0)

    perform_snowballing(doi_list_initial, starting_year, ending_year, authors, 'references', 0)



    # print("Backward Snowballing result")
    # print("References")
    # for i in final_result['references']['doi']:
    #     print(i)
    #
    # print("Forward Snowballing result")
    # print("Citations")
    # for x in final_result['citations']['doi']:
    #     print(x)
    #
    # print("References titles")
    #
    # for i in final_result['references']['title']:
    #     print(i)

    # print("Forward Snowballing result")
    # print("Citations titles")
    # for x in final_result['citations']['title']:
    #     print(x)


    # final_title = list(set(final_result['citations']['title']).union(final_result['references']['title']))
    #
    # final_doi = list(set(final_result['citations']['doi']).union(final_result['references']['doi']))


    # for i in range(len(final_doi)) :
    #
    #     print(final_doi[i] + "  " + final_title[i])

    for i in final_result['references'] :

        print(i + "   " + final_result['references'][i])


    temp_ref = final_result['references']

    temp_cite = final_result['citations']

    references_dict = {}

    citations_dict = {}

    for i in temp_ref:

        references_dict["https://dx.doi.org/" + i] = temp_ref[i]


    for i in temp_cite:

        citations_dict["https://dx.doi.org/" + i] = temp_cite[i]





    result_dict = Merge(references_dict,citations_dict)

    request.session['result_dict'] = result_dict










    return render(request,'users/snowballing.html',{'data': references_dict.items(),"data2":citations_dict.items()})



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


def search_coreAPI(doi_title_dict):
    lists = []

    parameter_values_list = [1, 10, '9ipXPomYaSrHLAIuONZfzUGk3t57RcBD']

    parameter_list = ['page', 'pageSize', 'apiKey']

    for i in doi_title_dict:

        query = doi_title_dict[i]

        url = 'https://core.ac.uk:443/api-v2/search/'

        parameters = {}

        for k in range(len(parameter_list)):
            key = parameter_list[k]

            value = parameter_values_list[k]

            parameters[key] = value

        parameters = urlencode(parameters, quote_via=quote)

        url += quote(query) + "?" + parameters

        # print(url)

        response = requests.get(url)

        content = response.json()
        print(content)

        if content.__contains__("data"):
            for j in content["data"]:

                if j['_source']['description']:
                    # print(i['_source']['description'])
                    lists.append([i, query, j['_source']['description']])

                    break

    return lists


def create_index(doi_title_abstract):
    schema = Schema(
        article_doi=ID(stored=True),
        article_title=ID(stored=True),
        article_abstract=TEXT(analyzer=StemmingAnalyzer(), stored=True)
    )

    ix = index.create_in("C:/Users/sahme/PycharmProjects/django_project/index_dir", schema)

    writer = ix.writer()

    for i in doi_title_abstract:
        writer.add_document(article_doi=u"" + i[0], article_title=u"" + i[1], article_abstract=u"" + i[2])

    writer.commit()

    return ix


def perform_search(ix, input_query):
    with ix.searcher() as searcher:

        query_parser = qparser.QueryParser("article_abstract", schema=ix.schema, termclass=q.Variations)

        # input_query = input("\nEnter query: ")

        query_user = query_parser.parse(input_query)

        # actual_query = input_query

        corrected = searcher.correct_query(query_user, input_query)

        if corrected.query != query_user:

            # choice = input("\nDid you mean " + corrected.string + "? ")

            choice = 'y'

            if choice == 'y':

                actual_query = corrected.string

            else:

                actual_query = corrected.string

        else:
            print("\nNo need to correct the query\n\n ")

            actual_query = input_query

        splitted_query = actual_query.split(" ")

        final_query = ""

        for i in splitted_query:
            final_query += "*" + i + "* OR "

        # actual_query = "*" + actual_query + "*"

        # print('\n' + final_query + '\n')

        query_user = query_parser.parse(final_query)

        results = searcher.search(query_user)

        print("\nTotal Documents Matched: " + str(len(results)))

        return_map = {}

        for result in results:
            return_map[result['article_doi']] = result['article_title']

    return return_map


def abstract(request):

    res_dict = request.session['result_dict']
    list_abstracts = search_coreAPI(res_dict)
    index = create_index(list_abstracts)

    word = request.session.get("Keyword")
    map_result = perform_search(index, word)

    # if request.method == 'POST':
    #     form = AbstractForm(request.POST)
    #     if form.is_valid():
    #         #query = input('Enter the query to be searched: ')

    #
    #
    #
    #
    #     else:
    #             #messages.error(request,f'Wrong Url')
    #             return render(request, 'users/abstract.html', {'form': form})

    del request.session['list']
    del request.session['author']
    del request.session['StartYear']
    del request.session['EndYear']




    return render(request, 'users/abstract.html', {'map_result': map_result.items()})


def searchposts(request):
    if(request.method == 'GET'):
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if(query is not None):
            lookups = Q(Title__icontains=query)
            results = Articles.objects.filter(lookups).distinct()
            context = {'results': results, 'submitbutton': submitbutton}

            return render(request, 'users/searchposts.html' ,context)

        else:
            return render(request,'users/searchposts.html')
    else:
        return render(request, 'users/searchposts.html')


def model_form_upload(request):
    form2 = []
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            form2 = Document
            print(form2.description)
            return savepdf(request)

    else:
        form = DocumentForm()
        return render(request, 'users/model_form_upload.html', {'form': form})

    return savepdf(request)

def savepdf(request):
    document = Document.objects.all()
    # print(document.description)
    print(type(document))
    return render(request, 'users/model_form_upload.html', { 'document' : document})


def search_database(request):
    if(request.method == 'POST'):
        query = request.POST.get('q')

        submitbutton = request.POST.get('submit-database')

        if(query is not None):
            lookups = Q(Title__icontains=query)
            results = Articles.objects.filter(lookups).distinct()
            context = {'results': results, 'submitbutton': submitbutton}

            return render(request, 'users/search_database.html' ,{'results': results})

        else:
            return render(request,'users/search_database.html')
    else:
        return render(request, 'users/search_database.html')

def search_snowballing(request):
    if(request.method == 'POST'):
        query = request.POST.get('q')

        submitbutton = request.POST.get('submit-snowballing')

        if(query is not None):
            lookups = Q(Title__icontains=query)
            results = Articles.objects.filter(lookups).distinct()
            context = {'results': results, 'submitbutton': submitbutton}

            return render(request, 'users/search_snowballing.html' ,{'results': results})

        else:
            return render(request,'users/search_snowballing.html')
    else:
        return render(request, 'users/search_snowballing.html')

