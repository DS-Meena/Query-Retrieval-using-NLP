from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from answer.forms import InputForm
from answer.compute import main
from answer.speech import say

# Base Case function
def index(request):
    # initial ans
    ans = None

    if 'submit' in request.POST:
        form = InputForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['ques']
            ans = main(ques)

    elif 'speak' in request.POST:
        error, response = say()
        if error:
            form = InputForm()
            ans = response
        else:
            ques = response
            form = InputForm(initial={'ques': ques})
            ans = main(ques)
    else:
        form = InputForm()  # take a blank form, and show

    context = {'form': form,
               'ans': ans}
    return render(request, 'page1.html', context)

def re_direct(request):
    return redirect("http://linkedin.com/in/d-s-m")