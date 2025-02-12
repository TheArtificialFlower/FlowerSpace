from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('bookmarks/', views.BookmarksView.as_view(), name="bookmarks"),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('otp/', views.UserOtpConfirm.as_view(), name='otp_check'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/edit/', views.UserProfileEdit.as_view(), name="profile_edit"),
    path('profile/follow/<str:username>/', views.UserRelation.as_view(), name="follow"),
    path('profile/<str:username>/', views.UserProfile.as_view(), name="profile"),
]