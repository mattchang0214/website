from accounts import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.home_redirect, name='home_redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^books/', include('books.urls')),
    url(r'^accounts/', include('accounts.urls')),
]
