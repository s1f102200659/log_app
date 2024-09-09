from django.contrib import admin
from log_app.models import Kindergarten, Student, StudentJournal, Caregiver, Journal

# Register your models here.
admin.site.register(Kindergarten)
admin.site.register(Student)
admin.site.register(StudentJournal)
admin.site.register(Caregiver)
admin.site.register(Journal)
