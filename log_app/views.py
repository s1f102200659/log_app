from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required, user_passes_test


from log_app.models import Student

# Create your views here.
def login(request):
    return render(request, 'log_app/login.html')

def home(request):
    return render(request, 'log_app/home.html')

def make_sharesheet(request):
    return render(request, 'log_app/make_sharesheet.html')

def make_caliculm(request):
    return render(request, 'log_app/make_caliculm.html')

#生徒一覧
class StudentList(ListView):
    model = Student
    template_name = 'log_app/student_list.html'
    context_object_name = 'students'

#生徒の詳細ページ
class StudentDetail(DetailView):
    model = Student
    context_object_name = 'student'

#生徒の追加・編集
# @login_required
# @user_passes_test(lambda u: u.is_admin)
class StudentCreate(CreateView):
    model = Student
    fields = "__all__"
    success_url = reverse_lazy('students')

class StudentUpdate(UpdateView):
    model = Student
    fields = "__all__"
    success_url = reverse_lazy('students')

class StudentDelete(DeleteView):
    model = Student
    fields = "__all__"
    success_url = reverse_lazy('students')
    context_object_name = 'student'

class CaregiverLoginView(LoginView):
    fields = "__all__"
    template_name = 'log_app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

from django.shortcuts import render
from .models import Student  # 生徒モデルをインポート

from django.http import JsonResponse

def search_students(request):
    query = request.GET.get('q')
    if query:
        results = Student.objects.filter(name__icontains=query)
        results_list = list(results.values('name', 'age', 'class_name'))  # 適切なフィールドをリスト化
        return JsonResponse({'results': results_list})
    return JsonResponse({'results': []})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.is_admin:
#                 return redirect('admin_dashboard')  # 管理者専用のダッシュボード
#             elif user.is_staff:
#                 return redirect('staff_dashboard')  # 保育士専用のダッシュボード
#             else:
#                 return redirect('home')  # 通常のユーザー
#         else:
#             return render(request, 'log_app/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'log_app/login.html')

# @login_required
# def admin_dashboard(request):
#     if not request.user.is_admin:
#         return redirect('home')
#     return render(request, 'log_app/admin_dashboard.html')

# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def staff_dashboard(request):
#     return render(request, 'log_app/staff_dashboard.html')
