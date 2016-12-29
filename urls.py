from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views

app_name = 'market'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login,{'template_name': 'market/login.html'} , name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'market:index'} , name='logout'),
    url(r'^password-change/$',
        auth_views.password_change, {
            'template_name': 'market/password_change.html',
            'post_change_redirect': 'market:password_change_done',
        }, name='password_change'),
    url(r'^password-change/done/$',
        auth_views.password_change_done, {
            'template_name': 'market/password_change_done.html'
        }, name='password_change_done'),
    url(r'^info-modify/$', views.InfoModify, name='info_modify'),
    url(r'^commodity/add$', views.CommodityAdd, name='commodity_add'),
    url(r'^commodity/(?P<pk>\d+)/$', views.CommodityView.as_view(), name='commodity_view'),
    url(r'^register/$', views.Register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
