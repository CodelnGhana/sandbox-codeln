from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Job, JobApplication
from .forms import JobForm

def job_list(request):
    jobs = Job.objects.all()
    developer = request.user
    applied_jobs = JobApplication.objects.filter(candidate=developer).all()
    return render(request, 'marketplace/developer/jobs/list.html',{'jobs': jobs, 'applied_jobs': applied_jobs})


def dev_job_detail(request,id):
    status = JobApplication.objects.filter(job_id=id).filter(candidate=request.user).all()
    job =Job.objects.get(id=id)
    return render(request, 'marketplace/developer/jobs/detail.html',
                  {'job': job,'status':status})


def recruiter_job_detail(request,id):
    job = Job.objects.get(id=id)

    selected_candidates = []
    applicants = []
    selected_devs = JobApplication.objects.filter(selected=True).all()
    for selectdev in selected_devs:
        selected_candidates.append(selectdev.candidate)
    all_devs = JobApplication.objects.filter(selected=False).all()
    for alldev in all_devs:
        applicants.append(alldev.candidate)

    recommended = [dev for dev in get_recommended_developers(job) if dev not in selected_candidates]

    return render(request, 'marketplace/recruiter/jobs/detail.html',
                  {'job': job, 'applicants': applicants, 'recommended': recommended, 'selected_candidates': selected_candidates})


def post_job(request):
    recruiter = request.user

    if request.method == 'POST':
        job_form = JobForm(data=request.POST)
        if job_form.is_valid():
            new_job = job_form.save(commit=False)
            new_job.posted_by = recruiter
            new_job.save()
            return HttpResponseRedirect("/marketplace/recruiter/manage_posted_jobs/")
    else:
        job_form = JobForm()
        return render(request, 'marketplace/recruiter/jobs/create.html', {'job_form': job_form})


def apply_for_job(request, job_id):
    if request.method == 'POST':
        job = Job.objects.get(id=job_id)
        newapply =JobApplication(candidate=request.user,job=job)
        newapply.save()
        return HttpResponseRedirect("/marketplace/dev/job_list/")
    else:
        return HttpResponseRedirect("/marketplace/dev/job_list/")


def manage_posted_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    job_details=[]
    for job in jobs:
        applied = JobApplication.objects.filter(job_id=job.id).all()
        app =applied.count()
        selected =JobApplication.objects.filter(job_id=job.id).filter(selected=True).all()
        sele=selected.count()
        job_details.append((job,app,sele))


    return render(request, 'marketplace/recruiter/jobs/list.html',{'job_details':job_details})


def pick_candidate(request, job_id, dev_id):
    job = Job.objects.get(id=job_id)
    dev =User.objects.get(id=dev_id)
    newpick = JobApplication(job=job,candidate=dev,selected=True)
    newpick.save()

    return HttpResponseRedirect("/marketplace/recruiter/manage_posted_jobs/")
def select_candidate(request, job_id, dev_id):
    candidate = User.objects.get(id=dev_id)
    job = JobApplication.objects.filter(job_id=job_id).filter(candidate=candidate).get()
    job.selected = True
    job.save()

    return HttpResponseRedirect("/marketplace/recruiter/manage_posted_jobs/")

def get_recommended_developers(job):
    allusers = User.objects.all()
    developers=[]
    for alluser in allusers:
        if alluser.profile.user_type =='developer':
            developers.append(alluser)


    recommended_developers = set()

    tech_stack = job.tech_stack.split(',')

    for developer in developers:
        if job.engagement_type == developer.profile.availabilty:
            recommended_developers.add(developer)
        elif job.job_role == developer.profile.language or job.job_role == developer.profile.framework:
            recommended_developers.add(developer)
        elif developer.profile.language in tech_stack or developer.profile.framework in tech_stack:
            recommended_developers.add(developer)
        elif job.location == developer.profile.country:
            recommended_developers.add(developer)
        elif (job.dev_experience == 'Entry' or job.dev_experience == 'Junior') and developer.profile.years == '1-2':
            recommended_developers.add(developer)
        elif (job.dev_experience == 'Junior' or job.dev_experience == 'Mid-Level') and developer.profile.years == '2-4':
            recommended_developers.add(developer)
        elif (job.dev_experience == 'Mid-Level' or job.dev_experience == 'Senior') and developer.profile.years == '4-above':
            recommended_developers.add(developer)
        else:
            pass

    return recommended_developers
