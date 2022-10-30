from django.shortcuts import get_object_or_404, redirect, render
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
        student_form = StudentForm(request.POST, prefix="student")
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

# the edit views are very similar to the create views
# and could probably be consolidated into a single view
# but my brain is too small to figure it out right now
def editStudentPageView(request, person_id):
    student = get_object_or_404(Student, pk=person_id)
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person", instance=student.person)
        student_form = StudentForm(request.POST, prefix="student", instance=student)
        if(person_form.is_valid() and student_form.is_valid()):
            person = person_form.save()
            student_form.instance.person_id = person.pk
            student = student_form.save()
            return redirect('index')
    else:
        person_form, student_form = PersonForm(prefix="person", instance=student.person), StudentForm(prefix="student", instance=student)

    context = {
        'title': 'Update Student',
        'forms': [person_form, student_form],
        'delete_url': f'/students/delete/{person_id}'
    }
    return render(request, 'form.html', context)

def deleteStudentPageView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("index")

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

def editInstructorPageView(request, person_id):
    instructor = get_object_or_404(Instructor, pk=person_id)
    if(request.method=="POST"):
        person_form = PersonForm(request.POST, prefix="person", instance=instructor.person)
        instructor_form = InstructorForm(request.POST, prefix="instructor", instance=instructor)
        if(person_form.is_valid() and instructor_form.is_valid()):
            person = person_form.save()
            instructor_form.instance.person_id = person.pk
            instructor = instructor_form.save()
            return redirect('index')
    else:
        person_form, instructor_form = PersonForm(prefix="person", instance=instructor.person), InstructorForm(prefix="instructor", instance=instructor)

    context = {
        'title': 'Update Instructor',
        'forms': [person_form, instructor_form],
        'delete_url': f'/instructors/delete/{person_id}'
    }
    return render(request, 'form.html', context)

def deleteInstructorPageView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("index")

def createEmploymentPageView(request):
    if(request.method == "POST"):
        employment_form = CreateEmploymentForm(request.POST, prefix="employment")
        if(employment_form.is_valid()):
            employment = employment_form.save()
            return redirect('index')
    else:
        employment_form = CreateEmploymentForm(prefix="employment")
    
    context = {
        'title': 'Create New Employment',
        'forms': [employment_form],
    }
    return render(request, 'form.html', context)

def editEmploymentPageView(request, employment_id):
    employment = get_object_or_404(Employment, pk=employment_id)
    if(request.method == "POST"):
        employment_form = UpdateEmploymentForm(request.POST, prefix="employment", instance=employment)
        if(employment_form.is_valid()):
            employment = employment_form.save()
            return redirect('index')
    else:
        employment_form = UpdateEmploymentForm(prefix="employment", instance=employment)
    
    context = {
        'title': 'Update Employment',
        'forms': [employment_form],
        'delete_url': f'/employments/delete/{employment_id}'
    }
    return render(request, 'form.html', context)

def deleteEmploymentPageView(request, employment_id):
    employment = get_object_or_404(Person, pk=employment_id)
    employment.delete()
    return redirect("index")