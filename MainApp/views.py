from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from datetime import date
from .mailer import send_email
from .utils import get_current_semester, get_notifications, get_notification_count
import csv
from django.http import HttpResponse

# Create your views here.
def indexPageView(request,semester_id=None):
    # don't show them the reminder notification for the remainder of the session
    if('show_reminder' not in request.session):
        request.session['show_reminder'] = True
    else:
        request.session['show_reminder'] = False

    if(semester_id == None):
        semester = get_current_semester()
    else:
        semester = Semester.objects.get(pk=semester_id)
    employments = semester.employment_set.all()
    context = {
        'employments': employments,
        'semester': semester,
        'semesters': Semester.objects.all(),
        'show_reminder': request.session['show_reminder']
    }
    return render(request, 'index.html', context)

def reportsPageView(request):
    num_females = 3
    num_males = 5
    context = {
        'gender': {
            'id': 'gender_chart',
            'labels': ['Males', 'Females'],
            'data': [num_males, num_females],
            'title': "Male/Female Ratio",
            'type': "pie",
            'colors': ['#6666cc','#cc6666']
        }
        # todo: add the other charts here
    }
    return render(request, 'reports.html', context)

def notificationsPageView(request):
    notifications = get_notifications()
    context = {
        'eform_notifications': notifications['eform'],
        'work_auth_notifications': notifications['work_auth'],
        'pay_increase_notifications': notifications['pay_increase'],
    }
    return render(request, 'notifications.html', context)

def testPageView(request):
    return render(request, 'test.html')

def updatePayRatePageView(request, employment_id):
    employment = get_object_or_404(Employment, pk=employment_id)
    if(request.method=="POST"):
        payrate_form = PayRateForm(request.POST)
        if(payrate_form.is_valid()):
            payrate = payrate_form.save(commit=False)
            payrate.employment = employment
            payrate.save()
            return redirect('index')
    else:
        payrate_form = PayRateForm()
    context = {
        'title': f'Update Pay Rate for {employment.__str__()}',
        'forms': [payrate_form],
        'info_title': 'Pay Rate History',
        'info': employment.payrate_set.all()
    }
    return render(request, 'form.html', context)

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
        'forms': [person_form, student_form],
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

            new_workauth_value = employment_form.cleaned_data['work_auth_received']
            previous_workauth_value = Employment.objects.get(pk=employment_id).work_auth_received

            employment = employment_form.save()

            # if previously NOT authorized but NOW authorized, send email
            if(new_workauth_value and not previous_workauth_value):
                send_email(
                    f'You are authorized to work',
                    f'{employment.student.person.full_name}, you are authorized to work as a {employment.position_type} for {employment.supervisor.person.full_name}. Have fun!',
                    'byu_information_systems_fake@fake.com',
                    [employment.student.person.email]
                )

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

def downloadEmployees(request, filter):

    if filter == "currentSemester":
        semester = get_current_semester()
        filename = "CurrentSemester_Employments.csv"
        records = semester.employment_set.all()
    elif filter == "supervisor":
        records = Employment.objects.all().order_by("supervisor__person__first_name")
        filename = "Employments_BySupervisor.csv"
    else:
        records = Employment.objects.all()
        filename = "All_Employments.csv"
    
    content_disposition = 'attachment; filename=' + filename
    response = HttpResponse(
        content_type = 'text/csv',
        headers={'Content-Disposition': content_disposition},
    )
    writer = csv.writer(response)

    
    
    writer.writerow(['Supervisor', 'Student Name',  'Expected Hours', 'Class Code', 'Position Type', 'Semesters', 'Hire Date', 'Terminated Date', 'Survey Sent', 'E-Form Submission', 'Work Auth Recceived', 'Name Change Complete', 'Notes'])
    
    for record in records:
        dataList = []
        dataList.append(record.supervisor)
        dataList.append(record.student)
        dataList.append(record.expected_hours)
        dataList.append(record.class_code)
        dataList.append(record.position_type)
        semesters = '| '
        for semester in record.semesters.all():
            semesters +=  str(semester) + ' | '
        dataList.append(semesters)
        dataList.append(record.hire_date)
        dataList.append(record.terminated_date)
        dataList.append(record.survey_sent)
        dataList.append(record.eform_submission)
        dataList.append(record.work_auth_received)
        dataList.append(record.name_change_complete)
        dataList.append(record.notes)
        writer.writerow(dataList)

    return response