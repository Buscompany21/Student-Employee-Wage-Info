from django import forms
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