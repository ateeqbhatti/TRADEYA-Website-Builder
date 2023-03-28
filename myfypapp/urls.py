from django.urls import path, include
from myfypapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from .views import contact
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('forms/data',views.contact_list, name='contact_list'),
    path('myapp/forms/',views.contact),
    path('form_new',views.form_new),
    path('editor',views.editor, name='editor'),
    path('',views.main),
    path('template1',views.template1),
    path('contact/<int:id>/view/', views.contact_detail, name='contact_detail'),
    path('contact/<int:id>/edit/', views.contact_update, name='contact_update'),
    path('contact/<int:id>/delete/', views.contact_delete, name='contact_delete'),
    path('contact/', contact, name='contact'),
    path('signup',views.signup, name='signup'),
    path('login',views.user_login, name='login'),
    path('logout',views.user_logout, name='login'),
    # path('loginp',views.loginpage, name='loginpage')

]

urlpatterns += staticfiles_urlpatterns()
