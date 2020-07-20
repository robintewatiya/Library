"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),


    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html')),

    path('logout/', LogoutView.as_view(template_name='library/index.html'), name='logout'),
    path('afterlogin', views.afterlogin_view),
    path('viewbook/delete/<int:book_id>', views.delete_book),
    path('viewissuedbook/delete/<int:isbn>', views.deassociate_book),

    #path('addrequest/<int:book_id>/<int:user_id>/', views.request_add_book),
    path('addrequest/<int:book_id>/<int:user_id>/', views.request_add_book, name='addrequest'),
    path('deleterequest/<int:book_id>/<int:user_id>/', views.request_delete_book, name='deleterequest'),
    path('approverequest/<int:book_id>/<int:user_id>/', views.approve_request, name='approverequest'),
    path('denyrequest/<int:book_id>/<int:user_id>/', views.deny_request, name='denyrequest'),
    #path(r'^viewlibrary/addrequest/(?P<book_id>\w+)/(?P<user_id>\w+)/$', views.request_add_book),

    path(r'addbook/', views.addbook_view, name='addbook'),
    path(r'viewbook/', views.viewbook_view, name='viewbook'),
    path(r'issuebook/', views.issuebook_view, name='issuebook'),
    path(r'viewissuedbook/', views.viewissuedbook_view, name='viewissuedbook'),
    path(r'viewstudent/', views.viewstudent_view, name='viewstudent'),
    path(r'viewlibrary/', views.viewlibrary_view, name='viewlibrary'),
    path(r'viewissuedbookbystudent/', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),
    path(r'viewrequestedbooks/', views.viewrequestedbooks, name='viewrequestedbooks'),
    path(r'viewpendingrequest/', views.viewpendingrequests, name='viewpendingrequest')

]
