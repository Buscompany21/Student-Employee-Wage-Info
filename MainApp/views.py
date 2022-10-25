from django.shortcuts import render
from .models import *

# Create your views here.
def indexPageView(request):
    students = Student.objects.all()
    instructors = Instructor.objects.all()
    context = {
        'students': students,
        'instructors': instructors
    }
    return render(request, 'index.html', context)

def testPageView(request):
    return render(request, 'test.html')