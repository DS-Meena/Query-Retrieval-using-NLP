from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http.response import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect

from answer.forms import InputForm
from answer.compute import main
#from answer.speech import say
from answer.speechWeb import convert

import os

# Base Case function
def index(request):
    # initial ans
    ans = None

    if 'submit' in request.POST:
        form = InputForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['ques']
            ans = main(ques)

    # for the post request in py audio
    # elif 'speak' in request.POST:
    #    error, response = say()
    #    if error:
    #        form = InputForm()
    #        ans = response
        else:
            ques = ""
            # ques = response
            form = InputForm(initial={'ques': ques})
            ans = main(ques)
    else:
        form = InputForm()  # take a blank form, and show

    context = {'form': form,
               'ans': ans}
    return render(request, 'page1.html', context)


def upload(request):
    if request.method == "POST":
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        savedAudio_path = os.path.join(BASE_DIR, "answer", "saved_data", "savedAudio.wav")


        customHeader = request.META['HTTP_MYCUSTOMHEADER']

        uploadedFile = open(savedAudio_path, "wb")
        # the actual file is in request.body
        uploadedFile.write(request.body)
        uploadedFile.close()

        error, response = convert()
        if error:
            form = InputForm()
            ans = response
            ques = ""
        else:
            ques = response
            form = InputForm(initial={'ques': ques})
            ans = main(ques)

        return JsonResponse({'success': True, 'ques': ques, 'ans': ans})

def re_direct(request):
    return redirect("http://linkedin.com/in/d-s-m")