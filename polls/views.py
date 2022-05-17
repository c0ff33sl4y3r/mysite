from django.http import HttpResponse, HttpResponseRedirect, Http404
from polls.models import Question, Choice
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic


def index(request):
    if request.user.is_authenticated:
        latest_question_list = Question.objects.order_by('id')[:]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)
    else:
        return redirect("login")


def detail(request, question_id):
    if request.user.is_authenticated:
        try:
            question = Question.objects.get(pk=question_i)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, 'polls/detail.html', {'question': question})
    else:
        return redirect("login")


def results(request, question_id):
    if request.user.is_authenticated:
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, 'polls/results.html', {'question': question})
    else:
        return redirect("login")

def vote(request, question_id):
    if request.user.is_authenticated:
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        return redirect("login")