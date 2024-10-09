# auth_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('<str:provider>/login/', views.OAuthLoginView.as_view(), name='oauth-login'),
    path('<str:provider>/callback/', views.OAuthCallbackView.as_view(), name='oauth-callback'),
    path('token/', views.TokenView.as_view(), name='token'),
]
