from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Gender)
admin.site.register(YearInProgram)
admin.site.register(Employment)
admin.site.register(PayRate)
admin.site.register(Semester)
admin.site.register(Season)
admin.site.register(PositionType)
admin.site.register(EmplRecord)