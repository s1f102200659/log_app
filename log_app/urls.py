from django.urls import path
from . import views
from .views import StudentList, StudentDetail, StudentCreate, StudentUpdate, StudentDelete, CaregiverLoginView
from django.conf import settings
from django.contrib.auth.views import LogoutView
# from django.conf.urls.static import static


urlpatterns = [
    path('',views.login),
    path('home/',views.home, name='home'),
    path('make_sharesheet',views.make_sharesheet, name='sharesheet'),
    path('check_sharesheet',views.check_sharesheet,name='check_sharesheet'),
    path('sheet_complate',views.complate,name='sheet_complate'),
    path('make_caliculm', views.make_caliculm, name='caliculm'),
    path('check/caliculm',views.check_caliculm,name='check_caliculm'),
    path('student_info', StudentList.as_view(), name='students'),
    path('student/<int:pk>/', StudentDetail.as_view(), name='student'),
    path('create-student/', StudentCreate.as_view(), name='create-student'),
    path('edit-student/<int:pk>/', StudentUpdate.as_view(), name='edit-student'),
    path('delete-student/<int:pk>/', StudentDelete.as_view(), name='delete-student'),
    path('login/', CaregiverLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),

]


    # path('', PostList.as_view(), name='posts'),
    # path('post/<int:pk>/', PostDetail.as_view(), name='post'),
    # path('edit-task/<int:pk>/', PostUpdate.as_view(), name='edit-task'),
    # path('create-post/', PostCreate.as_view(), name='create-post'),
    # path('delete-task/<int:pk>/', PostDelete.as_view(), name='delete-task'),
    # path('signup/', views.Signup.as_view(), name='signup'),
    # path('others/', views.others, name='others'),
