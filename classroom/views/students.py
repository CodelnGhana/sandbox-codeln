from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..decorators import student_required
from ..forms import TakeQuizForm
from ..models import Quiz, Student, TakenQuiz, User,StudentAnswer,Answer,Subject,RandomQuiz,Question
import random
from transactions.models import OpenCall

@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        queryset = Quiz.objects.all() \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()

        return context



@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset

# def taken_quizlist(request):
#     taken_quizzes =TakenQuiz.objects.filter(student_id=request.user.id)
#
#     return render(request, 'classroom/students/taken_quiz_list.html',{'taken_quizzes':taken_quizzes})


def student_registration(request):
    if Student.objects.filter(user_id=request.user.id).exists():
        return redirect('students:quiz_list')
    else:
        registration = Student(user=request.user)
        registration.save()
        return redirect('students:quiz_list')

@login_required
def take(request, pk):
    global tempquiz

    quiz = get_object_or_404(Quiz, pk=pk)
    student = Student.objects.get(user_id=request.user.id)
    correct_answers = StudentAnswer.objects.filter(quiz=quiz).filter(student=student).filter(answer__is_correct=True).count()
    questionlist = []
    try:
        tempquiz = RandomQuiz.objects.get(quiz_id=pk)
    except RandomQuiz.DoesNotExist:
        currentquiz =Question.objects.filter(quiz_id=pk)
        for onequestion in currentquiz:

            questionlist.append(onequestion.id)
        try:
            mell = random.sample(questionlist, 3)
            obj = RandomQuiz(quiz=quiz, student=student, questions=mell)
            obj.save()
            return redirect('students:take', pk)
        except:
            pass

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'classroom/students/taken_quiz.html')



    if not tempquiz.questions == None:
        tital =tempquiz.questions
        randlist =[]
        for x in tital:
            randlist.append(int(x))
        maswali =Question.objects.filter(id__in=randlist)
        total_questions = len(randlist)
        total_unanswered_questions = maswali.count()
        progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
        question = maswali.first()
        ile =[]
        ile.append(question.id)

        res = list(set(randlist) ^ set(ile))

        if request.method == 'POST':
            form = TakeQuizForm(question=question, data=request.POST)
            if form.is_valid():
                with transaction.atomic():
                    if 'answer' in request.POST:
                        student_answer = form.save(commit=False)
                        student_answer.student = student
                        student_answer.quiz = quiz
                        student_answer.save()
                        mimi = RandomQuiz.objects.get(quiz_id=pk)
                        mimi.questions = res
                        mimi.save()

                    else:
                        default_answer = StudentAnswer(quiz=quiz,student=student,answer=Answer.objects.filter(question_id = question.id).last())
                        default_answer.save()
                        mimi = RandomQuiz.objects.get(quiz_id=pk)
                        mimi.questions = res
                        mimi.save()
                    if student.get_unanswered_questions(quiz).exists():
                        return redirect('students:take', pk)
        else:
            form = TakeQuizForm(question=question)

        return render(request, 'classroom/students/take_quiz_form.html', {
            'quiz': quiz,
            'question': question,
            'form': form,
            'progress': progress
        })

    else:
        score = (correct_answers / 3) * 100
        TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
        return redirect('students:taken_quiz_list')


def retake(request,quizid,studentid):

    TakenQuiz.objects.filter(quiz_id=quizid,student_id=studentid).delete()
    StudentAnswer.objects.filter(quiz_id=quizid,student_id=studentid).delete()
    return redirect('students:take_quiz', quizid)
