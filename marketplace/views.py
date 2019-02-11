from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Job, Recruiter, Developer, JobApplication, Person
from .forms import JobForm


def user_dashboard(request):
    """a view to show developer's home on marketplace."""
    user_is_recruiter = False

    user = Person.objects.get(auth_user__username=request.user)

    user_has_posted_jobs = False

    try:
        if isinstance(user.recruiter, Recruiter):
            user_is_recruiter = True
            user_has_posted_jobs = True if Job.objects.filter(posted_by=user.recruiter).first() else False
    except:
        pass

    if user_is_recruiter:
        return render(request, 'marketplace/recruiter/home.html', {'user_has_posted_jobs': user_has_posted_jobs})
    return render(request, 'marketplace/developer/home.html')


def job_list(request):
    """a view to display the list of jobs."""
    jobs = Job.objects.all()

    developer = Developer.objects.get(auth_user__username=request.user)

    applied_jobs = developer.applied_jobs.all()

    return render(request, 'marketplace/developer/jobs/list.html',
                  {'jobs': jobs, 'applied_jobs': [j_a.job for j_a in applied_jobs]})


def dev_job_detail(request, year, month, day, job):
    """a view to display details of a single job."""
    job = get_object_or_404(
        Job,
        slug=job,
        position_filled=False,
        created__year=year,
        created__month=month,
        created__day=day
    )

    applied = True if request.GET['applied'] == 'True' else False

    return render(request, 'marketplace/developer/jobs/detail.html',
                  {'job': job, 'job_applied_status': applied})


def recruiter_job_detail(request):
    """a view to display job_details of a single job."""
    job = Job.objects.get(id=request.GET['job_id'])

    applicants = []

    devs = request.GET['list_of_applicants'].split(",")
    for dev in devs:
        try:
            applicants.append(Developer.objects.get(auth_user__username=dev))
        except:
            pass

    return render(request, 'marketplace/recruiter/jobs/detail.html',
                  {'job': job, 'applicants': applicants})


def post_job(request):
    """a view to post a job."""
    recruiter = Recruiter.objects.get(auth_user__username=request.user)

    if request.method == 'POST':
        job_form = JobForm(data=request.POST)
        if job_form.is_valid():
            new_job = job_form.save(commit=False)
            new_job.posted_by = recruiter
            new_job.save()
            # job_form = JobForm()
            return HttpResponseRedirect("/marketplace/recruiter/manage_posted_jobs/")
    else:
        job_form = JobForm()
        return render(request, 'marketplace/recruiter/jobs/create.html', {'job_form': job_form})


def apply_for_job(request, job_id):
    """a view to apply for a job."""
    if request.method == 'POST':
        job = Job.objects.get(id=job_id)

        developer = Developer.objects.get(auth_user__username=request.user)

        developer.applied_jobs.get_or_create(job=job)

        return HttpResponseRedirect("/marketplace/dev/job_list/")
    else:
        return HttpResponseRedirect("/marketplace/dev/job_list/")


def manage_posted_jobs(request):
    """a view to display the list of jobs."""
    jobs = Job.objects.filter(posted_by=Recruiter.objects.get(auth_user__username=request.user))

    job_details = []

    for job in jobs:
        try:
            temp = JobApplication.objects.get(job=job).applied_by.all()
        except:
            temp = None

        if temp:
            applied_by = [dev for dev in temp]
        else:
            applied_by = []

        job_details.append((job, applied_by))

    return render(request, 'marketplace/recruiter/jobs/list.html',
                  {'job_details': job_details})