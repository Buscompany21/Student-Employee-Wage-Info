from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('', views.indexPageView, name="index"),
  path('reports', views.reportsPageView, name="reports"),
  path('notifications', views.notificationsPageView, name="notifications"),
  path('semesters/<int:semester_id>', views.indexPageView, name="index"),
  path('test-page', views.testPageView, name="test"),
  path('students/create', views.createStudentPageView, name="create-student"),
  path('students/edit/<int:person_id>', views.editStudentPageView, name='edit-student'),
  path('students/delete/<int:person_id>', views.deleteStudentPageView, name="delete-student"),
  path('instructors/create', views.createInstructorPageView, name="create-instructor"),
  path('instructors/edit/<int:person_id>', views.editInstructorPageView, name="edit-instructor"),
  path('instructors/delete/<int:person_id>', views.deleteInstructorPageView, name="delete-instructor"),
  path('employments/create', views.createEmploymentPageView, name="create-employment"),
  path('employments/edit/<int:employment_id>', views.editEmploymentPageView, name="edit-employment"),
  path('employments/delete/<int:employment_id>', views.deleteEmploymentPageView, name="delete-instructor"),
  path('payrate/update/<int:employment_id>', views.updatePayRatePageView, name="update-payrate"),
  path('employees/download/<str:filter>', views.downloadEmployees, name="download-employees"),
]