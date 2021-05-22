from django.urls import path
from django.conf.urls import url
from .views import RegisterUser, BlacklistTokenUpdateView,VerificationView,UserProfileAPI,AdminProfileView,PasswordResetAPIView,PasswordResetConfirmView
app_name = 'users'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="create_user"),
    path('dashboard/',UserProfileAPI.as_view(),name="dashboard"),
    url('dashboard-admin/',AdminProfileView.as_view(),name="dashboard-admin"),

    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),name='blacklist'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate'),
    path('password_reset/',PasswordResetAPIView.as_view(),name='password_change'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]
