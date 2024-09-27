from django.urls import path, include
from . import views
from .views import (
    StudentList, StudentDetail, StudentCreate, StudentUpdate, StudentDelete,
    CaregiverLoginView, admin_dashboard, caregiver_dashboard, CaregiverStudentList,
    KindergartenList, KindergartenCreate, KindergartenUpdate, KindergartenDelete,
    CaregiverList, CaregiverCreate, CaregiverUpdate, CaregiverDelete
    )
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',include('accounts.urls', namespace='accounts')),
    path('header/url/', views.header_view, name='header'),
    # path('home/',views.home, name='home'),
    path('make_sharesheet',views.make_sharesheet, name='sharesheet'),
    path('check_sharesheet',views.check_sharesheet,name='check_sharesheet'),
    path('sheet_complate',views.complate,name='sheet_complate'),
    path('make_caliculm', views.make_caliculm, name='caliculm'),
    path('check/caliculm',views.check_caliculm,name='check_caliculm'),
    path('student_info', StudentList.as_view(), name='students'),
    path('caregiver/student_info/', CaregiverStudentList.as_view(), name='caregiver_students'),
    path('student/<int:pk>/', StudentDetail.as_view(), name='student'),
    path('create-student/', StudentCreate.as_view(), name='create-student'),
    path('edit-student/<int:pk>/', StudentUpdate.as_view(), name='edit-student'),
    path('delete-student/<int:pk>/', StudentDelete.as_view(), name='delete-student'),

    # 園情報管理
    path('kindergarten/', KindergartenList.as_view(), name='kindergarten_list'),
    path('kindergarten/create/', KindergartenCreate.as_view(), name='create-kindergarten'),
    path('kindergarten/edit/<int:pk>/', KindergartenUpdate.as_view(), name='edit-kindergarten'),
    path('kindergarten/delete/<int:pk>/', KindergartenDelete.as_view(), name='delete-kindergarten'),

    # 保育士管理
    path('caregivers/', CaregiverList.as_view(), name='caregiver_list'),
    path('caregivers/create/', CaregiverCreate.as_view(), name='create-caregiver'),
    path('caregivers/edit/<int:pk>/', CaregiverUpdate.as_view(), name='edit-caregiver'),
    path('caregivers/delete/<int:pk>/', CaregiverDelete.as_view(), name='delete-caregiver'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('caregiver_dashboard/', caregiver_dashboard, name='caregiver_dashboard'),
    path('login/', CaregiverLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
    path('students/', StudentList.as_view(), name='student-list'),
]



    # path('', PostList.as_view(), name='posts'),
    # path('post/<int:pk>/', PostDetail.as_view(), name='post'),
    # path('edit-task/<int:pk>/', PostUpdate.as_view(), name='edit-task'),
    # path('create-post/', PostCreate.as_view(), name='create-post'),
    # path('delete-task/<int:pk>/', PostDelete.as_view(), name='delete-task'),
    # path('signup/', views.Signup.as_view(), name='signup'),
    # path('others/', views.others, name='others'),
