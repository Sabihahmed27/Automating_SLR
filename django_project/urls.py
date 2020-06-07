"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users.views import searchposts

urlpatterns = [
    # path('', user_views.data, name='scholar'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('review/', user_views.review, name='review'),
    path('bib-tex/<key>/',user_views.get_bib_tex, name='bib_tex'),
    path('journals/', user_views.journal_list, name='journal_list'),
    path('journals_history/', user_views.journal_history, name='journal_history'),
    path('profile/<username>/',user_views.testing),
    path('journals_delete/<key>/', user_views.journal_deleteOne,name='journal_history'),
    path('journals_delete/', user_views.journal_delete, name='journal_history'),
    path('journals/upload', user_views.upload_journal, name='upload_journal'),
    path('database/', user_views.scholarly_data , name='database'),
    path('abstract/', user_views.abstract, name='abstract'),
    path('fulltext/',user_views.fulltext,name='fulltext'),
    path('model_form_upload/', user_views.model_form_upload,name = 'model_form_upload'),
    path('query/<str:data>', user_views.query, name='query'),
    path('searchposts/', user_views.searchposts, name='searchposts'),
    path('search_database/',user_views.search_database,name='search_database'),
    path('search_snowballing/',user_views.search_snowballing,name='search_snowballing'),
    path('scholar/', user_views.data, name='scholar'),
    path('quality-assessment/',user_views.quality_assessment,name="quality_assessment"),
    path('snowballing/', user_views.snowballing, name='snowballing'),
    path('snowballing/<key>',user_views.snowballing_one, name='snowballing_one'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', include('blog.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


