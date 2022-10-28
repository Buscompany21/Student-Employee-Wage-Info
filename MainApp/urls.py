from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('', views.indexPageView, name="index"),
  path('test-page', views.testPageView, name="test"),
  path('students/create', views.createStudentPageView, name="create-student"),
  path('students/edit/<int:person_id>', views.editStudentPageView, name='edit-student'),
  path('instructors/create', views.createInstructorPageView, name="create-instructor"),
  path('instructors/edit/<int:person_id>', views.editInstructorPageView, name="edit-instructor"),
  path('employments/create', views.createEmploymentPageView, name="create-employment"),
  path('employments/edit/<int:employment_id>', views.editEmploymentPageView, name="edit-employment"),
]