from django.shortcuts import redirect, render
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
        person_form = PersonForm(request.POST, prefix="person")
        student_form = StudentForm(request.POST, prefix="instructor")
        if(person_form.is_valid() and student_form.is_valid()):
            person = person_form.save()
            student_form.instance.person_id = person.pk
            student = student_form.save()
            return redirect('index')
    else:
        person_form, student_form = PersonForm(prefix="person"), StudentForm(prefix="student")

    context = {
        'title': 'Create New Student',
        'forms': [person_form, student_form]
    }
    return render(request, 'form.html', context)

def createInstructorPageView(request):
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person")
        instructor_form = InstructorForm(request.POST, prefix="instructor")
        if(person_form.is_valid() and instructor_form.is_valid()):
            person = person_form.save()
            instructor_form.instance.person_id = person.pk
            instructor = instructor_form.save()
            return redirect('index')
    else:
        person_form, instructor_form = PersonForm(prefix="person"), InstructorForm(prefix="instructor")

    context = {
        'title': 'Create New Instructor',
        'forms': [person_form, instructor_form]
    }
    return render(request, 'form.html', context)

def createEmploymentPageView(request):
    if(request.method == "POST"):
        employment_form = EmploymentForm(request.POST, prefix="employment")
        if(employment_form.is_valid()):
            employment = employment_form.save()
            return redirect('index')
    else:
        employment_form = EmploymentForm(prefix="employment")
    
    context = {
        'title': 'Create New Employment',
        'forms': [employment_form]
    }
    return render(request, 'form.html', context)