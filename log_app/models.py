from django.db import models

# 園テーブル
class Kindergarten(models.Model):
    kindergarten_id = models.AutoField(primary_key=True)  # 園ID (PK)
    postal_code = models.CharField(max_length=20)  # 郵便番号
    password = models.CharField(max_length=128)  # パスワード
    policy = models.TextField()  # 方針
    name = models.CharField(max_length=100)  # 園の名前

    def __str__(self):
        return self.name


# 保育士テーブル
class Caregiver(models.Model):
    caregiver_id = models.AutoField(primary_key=True)  # 保育士ID (PK)
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
    name = models.CharField(max_length=100)  # 名前
    grade = models.IntegerField()  # 学年

    def __str__(self):
        return self.name


# 生徒テーブル
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # 生徒ID (PK)
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.SET_NULL, null=True)  # 保育士ID (FK)
    name = models.CharField(max_length=100)  # 生徒の名前
    birth_date = models.DateField()  # 生年月日
    allergy_info = models.TextField(blank=True, null=True)  # アレルギー
    additional_info = models.TextField(blank=True, null=True)  # 生徒の情報

    def __str__(self):
        return self.name


# 生徒日誌テーブル
class StudentJournal(models.Model):
    journal_id = models.AutoField(primary_key=True)  # ID (PK)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # 生徒ID (FK)
    student_info = models.TextField()  # 生徒の情報
    date = models.DateField()  # 日付

    def __str__(self):
        return f"{self.student.name} - {self.date}"


# 日誌テーブル
class Journal(models.Model):
    journal_id = models.AutoField(primary_key=True)  # ID (PK)
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)  # 園ID (FK)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)  # 保育士ID (FK)
    date = models.DateField()  # 日付
    shared_sheet = models.TextField()  # 共有シート

    def __str__(self):
        return f"Journal {self.journal_id} for {self.kindergarten.name} on {self.date}"
