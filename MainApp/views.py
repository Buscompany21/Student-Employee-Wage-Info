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
        print("This data was submitted in the form: ", list(request.POST.items))
    # todo: create person record
    # then create student record

    context = {
        'title': 'Create New Student',
        'forms': [PersonForm(prefix="person"), StudentForm(prefix="student")]
    }
    return render(request, 'form.html', context)

def createInstructorPageView(request):
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person")
        instructor_form = InstructorForm(request.POST, prefix="instructor")
        if(person_form.is_valid and instructor_form.is_valid):
            person = person_form.save()
            instructor_form.instance.person_id = person.pk
            instructor = instructor_form.save()
            return redirect('index')

    context = {
        'title': 'Create New Instructor',
        'forms': [PersonForm(prefix="person"), InstructorForm(prefix="instructor")]
    }
    print(context['forms'][1])
    return render(request, 'form.html', context)