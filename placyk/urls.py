"""placyk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from placyk_app.views import HomeView, UserRegisterView, ChildRegisterView, HomeLogView, MessageView, NewMessageView, UserMessagesView,\
    LogoutView, AddVisitView, LoginView, UserView, ResetPasswordView, DeleteVisitView, EditVisitView
from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'^register_child/(?P<id>\d+)/$', ChildRegisterView.as_view(), name='register_child'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^home_login/$', HomeLogView.as_view(), name='home_login'),
    url(r'^details_message/(?P<id>\d+)/$', MessageView.as_view(), name='details_message'),
    url(r'^new_message/(?P<id>\d+)/?$', NewMessageView.as_view(), name='new_message'),
    url(r'^user_messages/(?P<id>\d+)/?$', UserMessagesView.as_view(), name='user_messages'),
    url(r'^logout/(?P<id>\d+)/$', LogoutView.as_view(), name='logout'),
    url(r'^add_visit/(?P<id>\d+)/?$', AddVisitView.as_view(), name='add_visit'),
    url(r'^user_site/(?P<id>\d+)/?$', UserView.as_view(), name='user_site'),
    url(r'^reset_password/(?P<id>\d+)/?$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^delete_visit/(?P<id>\d+)/?$', DeleteVisitView.as_view(), name='delete_visit'),
    url(r'^edit_visit/(?P<id>\d+)/?$', EditVisitView.as_view(), name='edit_visit'),
    url('^social', include('social_django.urls', namespace='social')),

]


