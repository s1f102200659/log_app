from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser

#園テーブル
class Kindergarten(models.Model):
    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    policy = models.TextField()

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    allergy_info = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    kindergarten = models.ForeignKey('Kindergarten', on_delete=models.CASCADE)
    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'caregiver'}
    )

    def __str__(self):
        return self.name


# 生徒日誌テーブル
class StudentJournal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_info = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.date}"

# 日誌テーブル
class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園
    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'caregiver'}
    )  # 保育士
    date = models.DateField()  # 日付
    shared_sheet = models.TextField()  # 共有シート
    students_condition = models.TextField()  # その日の生徒の様子を保管するフィールドを追加

    def __str__(self):
        return f"Journal for {self.kindergarten.name} on {self.date}"



# # 園テーブル
# class Kindergarten(models.Model):
#     kindergarten_id = models.AutoField(primary_key=True)  # 園ID (PK)
#     postal_code = models.CharField(max_length=20)  # 郵便番号
#     password = models.CharField(max_length=128)  # パスワード
#     policy = models.TextField()  # 方針
#     name = models.CharField(max_length=100)  # 園の名前

#     def __str__(self):
#         return self.name


# # 保育士テーブル
# class Caregiver(models.Model):
#     caregiver_id = models.AutoField(primary_key=True)  # 保育士ID (PK)
#     kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
#     name = models.CharField(max_length=100)  # 名前
#     grade = models.IntegerField()  # 学年

#     def __str__(self):
#         return self.name

#保育士テーブル
# class Caregiver(models.Model):
#     user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
#     grade = models.IntegerField()

#     def __str__(self):
#         return self.user.name


# 生徒テーブル
# class Student(models.Model):
#     student_id = models.AutoField(primary_key=True)  # 生徒ID (PK)
#     kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
#     # caregiver = models.ForeignKey(Caregiver, on_delete=models.SET_NULL, null=True)  # 保育士ID (FK)
#     name = models.CharField(max_length=100)  # 生徒の名前
#     birth_date = models.DateField()  # 生年月日
#     allergy_info = models.TextField(blank=True, null=True)  # アレルギー
#     additional_info = models.TextField(blank=True, null=True)  # 生徒の情報

#     def __str__(self):
#         return self.name


# # 日誌テーブル
# class Journal(models.Model):
#     journal_id = models.AutoField(primary_key=True)  # ID (PK)
#     kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
#     caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)  # 保育士ID (FK)
#     date = models.DateField()  # 日付
#     shared_sheet = models.TextField()  # 共有シート

#     def __str__(self):
#         return f"Journal {self.journal_id} for {self.kindergarten.name} on {self.date}"