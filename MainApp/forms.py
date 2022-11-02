from django import forms
from .models import *
from crispy_forms.helper import FormHelper

# this class just makes it so you can render multiple forms inside a single form tag
# (so we can do things like create a person object and a student object at the same time)
class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

class PersonForm(BaseForm):
    class Meta:
        model = Person
        fields = "__all__"

class StudentForm(BaseForm):
    class Meta:
        model = Student
        exclude=('person',)

class InstructorForm(BaseForm):
    class Meta:
        model = Instructor
        exclude=('person',)

class CreateEmploymentForm(BaseForm):
    class Meta:
        model = Employment
        exclude = ('terminated_date', 'survey_sent', 'eform_submission', 'work_auth_received', 'name_change_complete')
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'})
        }

class UpdateEmploymentForm(BaseForm):
    class Meta:
        model = Employment
        fields = '__all__'
        # show date inputs instead of plain text ones
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date',}),
            'terminated_date': forms.DateInput(attrs={'type': 'date'}),
            'survey_sent': forms.DateInput(attrs={'type': 'date'}),
            'eform_submission': forms.DateInput(attrs={'type': 'date'}),
            'work_auth_received': forms.DateInput(attrs={'type': 'date'}),
        }

class PayRateForm(BaseForm):
    class Meta:
        model = PayRate
        fields = "__all__"
        exclude = ("employment","input_date")
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',}),
        }