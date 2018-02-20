from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    # /books/
    url(r'^$', views.home, name='home'),
    # /books/all/
    url(r'^all/$', views.index, name='all'),
    # /books/mine/
    url(r'^mine/$', views.my_books, name='mine'),
    # /books/1/
    # url(r'^(?P<book_id>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<book_id>[0-9]+)/edit/$', views.update_book, name='update_book'),
    url(r'^(?P<book_id>[0-9]+)/delete/$', views.delete_book, name='delete_book'),
    url(r'^sell/$', views.create_book, name='create_book'),
    url(r'^results/', views.search, name='search'),
]
