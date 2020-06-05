from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse     # for the response
from answer.forms import InputForm
from answer.compute import main

def index(request):
    # initial ans
    ans = None
    # if user entered the input,  request method will be post
    if request.method == 'POST':

        form = InputForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['ques']
            ans = main(ques)
    else:
        form = InputForm()  # interact, show this page

    context = {'form': form,
               'ans': ans}
    return render(request, 'page1.html', context)
