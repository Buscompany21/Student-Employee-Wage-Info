from .models import Semester, Employment, PayRate
from datetime import date, timedelta
from django.utils import timezone

def get_current_semester():
    latest = Semester.objects.filter(start_date__lte=date.today()).latest('start_date')
    return latest

def get_notifications():
    notifications = {
        'eform': [],
        'work_auth': [],
        'pay_increase': [],
    }
    today = timezone.now()
    # notify if EForm field is unchecked 1 week after sending them the Qualtrics survey
    # get list of all employments which have survey_sent between 1 week ago and today's date that has a null eform_submission value
    notifications['eform'] = Employment.objects.filter(survey_sent__lte=today - timedelta(days=7), eform_submission=None)

    # notify if authorized to work hasn't been checked after 1 week
    # this is pretty similar to the EForm notifications
    notifications['work_auth'] = Employment.objects.filter(survey_sent__lte=today - timedelta(days=7), work_auth_received=None)

    # pay increase reminders at the beginning of each semester
    # 1. Get the current semester
    # 2. Get list of all employments that do NOT have a PayRate model
    # attached to them with a date value that falls in the bounds of the current semester
    current_semester = get_current_semester()
    # all the employments that HAVE gotten a raise
    relevant_employments = Employment.objects.filter(semesters__id=current_semester.id)
    raise_employment_ids = {r.employment.id for r in PayRate.objects.filter(effective_date__gte=current_semester.start_date).select_related('employment')}
    no_raise_employments = relevant_employments.exclude(id__in=raise_employment_ids)
    notifications['pay_increase'] = no_raise_employments
    return notifications

def get_notification_count(request):
    notifications = get_notifications()
    return {
        "NOTIFICATION_COUNT": len(notifications['pay_increase']) + len(notifications['work_auth']) + len(notifications['eform'])
    }
