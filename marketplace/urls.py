from django.urls import path

from . import views

app_name = 'marketplace'

urlpatterns = [

    path('dev/job_list/', views.job_list, name='job_list'),
    path('dev/job_detail/<int:id>', views.dev_job_detail, name='dev_job_detail'),
    path('dev/apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),

    path('recruiter/post_job/', views.post_job, name='post_job'),
    path('recruiter/manage_posted_jobs/', views.manage_posted_jobs, name='manage_posted_jobs'),
    path('recruiter/job_detail/<int:id>/', views.recruiter_job_detail, name='recruiter_job_detail'),
    path('recruiter/pick_candidate/<int:job_id>/<int:dev_id>/', views.pick_candidate, name='pick_candidate'),
    path('recruiter/select_candidate/<int:job_id>/<int:dev_id>/', views.select_candidate, name='select_candidate'),
]
