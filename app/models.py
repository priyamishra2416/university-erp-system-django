from django.db import models


class Student(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    roll = models.CharField(max_length=20)

    department = models.CharField(max_length=100)

    semester = models.IntegerField()

    def __str__(self):
        return self.name
class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20
    )

    def __str__(self):
        return f'{self.student.name} - {self.status}'

  
class Result(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)

    marks = models.IntegerField()

    cgpa = models.FloatField()

    def __str__(self):
        return f'{self.student.name} - {self.subject}'
class Fees(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    status = models.CharField(
        max_length=20
    )

    date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.student.name

     
class Faculty(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    department = models.CharField(max_length=100)

    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Timetable(models.Model):

    day = models.CharField(max_length=50)

    subject = models.CharField(max_length=100)

    faculty = models.CharField(max_length=100)

    time = models.CharField(max_length=50)

    def __str__(self):

        return self.subject
