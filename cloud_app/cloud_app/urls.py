from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    #path('signup', views.signup, name='signup'),
    #path('register/', views.registerView, name='register'),
    #path('login/', LoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(next_page='dashboard'), name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),
]
