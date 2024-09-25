from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('caregiver_dashboard')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
