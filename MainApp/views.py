from django.shortcuts import render
from .models import *
from .forms import *

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

def createStudentPageView(request):
    if(request.method=="POST"):
        print("This data was submitted in the form: ", list(request.POST.items))
    # todo: create person record
    # then create student record

    context = {
        'title': 'Create New Student',
        'forms': [PersonForm, StudentForm]
    }
    return render(request, 'form.html', context)

def createInstructorPageView(request):
    if(request.method=="POST"):
        print("This data was submitted in the form: ", list(request.POST.items))

    context = {
        'title': 'Create New Instructor',
        'forms': [PersonForm, InstructorForm]
    }
    print(context['forms'][1])
    return render(request, 'form.html', context)