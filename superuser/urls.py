from django.urls import path, include
from django.contrib.auth import views
from .views import (
    SendVerificationEmailView,
    RegisterAPIView, change_password, RegistrationView,
    UserLogInView, UserLogoutView, UserDetailView, send_email_view
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/password/change/', change_password),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('send-verification-email/', SendVerificationEmailView.as_view(), name='send_verification_email'),
    path('register-api/', RegisterAPIView.as_view(), name='register_api'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify_email/', SendVerificationEmailView.as_view(), name='verify_email'),
    path('admin/', send_email_view,name='superuser'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLogInView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
