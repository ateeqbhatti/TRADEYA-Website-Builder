from django.urls import path, include
from myfypapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
# from .views import contact
from django.contrib.auth.decorators import login_required
from .views import profile_add, profile_view
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

handler404 = 'myfypapp.views.error_404_view'


urlpatterns = [
    
    #Rendering Editor Builder
    path('editor', views.editor, name='editor'),
    
    #Rendering Main Page
    path('', views.main),
    
    #Rendering Signup Function
    path('signup', views.signup, name='signup'),
    
    #Rendering Login Functions
    path('login', views.user_login, name='login'),
    path('login2', views.user_login2, name='login2'),
    path('login3', views.user_login3, name='login3'),
    
    #Rendering Logout Function
    path('logout', views.user_logout, name='logout'),
    
    #Rendering Profile Data Function
    path('profile/add/', profile_add, name='profile_add'),
    
    #Rendering Profile Data View Function
    path('profile/', profile_view, name='profile'),
    
    #Rendering Template List View Function
    path('template_view', views.template_view, name='template_view'),
    
    #Rendering Change password Function
    path('change-password/', auth_views.PasswordChangeView.as_view(
         template_name='change_password.html',
         success_url='/password-changed/'), name='password_change'),
    path('password-changed/', views.password_changed, name='password_changed'),
    
    #Rendering Template Lists
    path('template2', views.template2, name='template2'),
    path('template3', views.template3, name='template3'),
    path('template1', views.template1, name='template1'),
    path('template4', views.template4, name='template4'),
    path('chatbot',views.chatbot, name='chatbot')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
