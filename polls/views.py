# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
# from django.http import Http404

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    Choice.votes = F("vote") + 1 # 경쟁 조건 회피 F함수 사용
    template_name = "polls/results.html"
    

def vote(request, question_id):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"]) # form태그에서 POST방식으로 보낸 데이터 'input태그의 name이 choice'를 가져와라
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRediret after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            # POST로 뷰가 호출된 경우에는 'HttpResponseRedirect'를 사용해 준다. (POST와 세트라고 생각하면 됨.)
            return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))
            # url을 하드코딩 하지 않기 위해 reverse를 사용