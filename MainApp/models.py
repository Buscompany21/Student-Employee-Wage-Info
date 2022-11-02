from multiprocessing import current_process
from django.db import models
import datetime
from django.utils import timezone
today = timezone.now

# Create your models here.

class Gender(models.Model):
    name = models.CharField(max_length = 30)
    def __str__(self):
        return self.name

class YearInProgram(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class PositionType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Semester(models.Model):
    start_date = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.RESTRICT)
    def __str__(self):
        return f'{self.season.__str__()} {self.start_date.strftime("%Y")}'

class EmplRecord(models.Model):
    value = models.IntegerField()
    def __str__(self):
        return str(self.value)

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    byu_name = models.CharField(max_length=200)
    gender = models.ForeignKey(Gender, null=False, on_delete=models.RESTRICT)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    byu_id = models.CharField(max_length=9)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name

# Student class inherits from Person class
# but instead of doing class Student(Person), we're doing the inheritance manually for more control
class Student(models.Model):
    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)
    international = models.BooleanField()
    year_in_program = models.ForeignKey(YearInProgram, on_delete=models.RESTRICT)
    pay_grad_tuition = models.BooleanField()

    def __str__(self):
        return self.person.__str__()

# Instructor class also inherits form Person class
class Instructor(models.Model):
    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.__str__()

class Employment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    expected_hours = models.DecimalField(max_digits=3, decimal_places=1)
    class_code = models.CharField(max_length=50, null=True, blank=True)
    position_type = models.ForeignKey(PositionType, on_delete=models.RESTRICT)
    empl_record = models.ForeignKey(EmplRecord, on_delete=models.RESTRICT)
    semesters = models.ManyToManyField(Semester)
    hire_date = models.DateField(default=today)
    terminated_date = models.DateField(null=True, blank=True)
    survey_sent = models.DateTimeField(null=True, blank=True)
    eform_submission = models.DateTimeField(null=True, blank=True)
    work_auth_received = models.DateTimeField(null=True, blank=True)
    name_change_complete = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    @property
    def current_pay_rate(self):
        return self.payrate_set.latest('effective_date')

    @property
    def pay_increase_amount(self):
        try:
            previous_pay_rate = self.payrate_set.order_by('-effective_date')[1]
            print(self.current_pay_rate.pay_rate-previous_pay_rate.pay_rate)
            return self.current_pay_rate.pay_rate - previous_pay_rate.pay_rate
        except Exception:
            return None

    def __str__(self):
        return f'{self.student.person.full_name} ({self.position_type.name} for {self.supervisor.person.full_name})'

class PayRate(models.Model):
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2)
    effective_date = models.DateTimeField()
    input_date = models.DateTimeField(default=today)
    employment = models.ForeignKey(Employment, on_delete=models.CASCADE)
    def __str__(self):
        return f'${self.pay_rate} for {self.employment.student.person.full_name} in {self.employment.class_code}'