from django.db import models

# Create your models here.

# 園テーブル
class Garden(models.Model):
    garden_id = models.AutoField(primary_key=True)
    postal_code = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    policy = models.TextField()
    garden_name = models.CharField(max_length=100)

    def __str__(self):
        return self.garden_name

# 生徒テーブル
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="students")
    student_name = models.CharField(max_length=100)
    grade = models.IntegerField()
    student_info = models.TextField()

    def __str__(self):
        return self.student_name

# 生徒日誌テーブル
class StudentJournal(models.Model):
    studentjournal_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentjournals")
    journal_info = models.TextField()

    def __str__(self):
        return f"Journal for {self.student.student_name}"

# 保育士テーブル
class Caretaker(models.Model):
    caretaker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="caretakers")
    grade = models.IntegerField()

    def __str__(self):
        return self.name

# 日誌テーブル
class Journal(models.Model):
    journal_id = models.AutoField(primary_key=True)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="journals")
    grade = models.IntegerField()

    def __str__(self):
        return f"Journal {self.journal_id} for Garden {self.garden.garden_name}"