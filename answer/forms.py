from django import forms

class InputForm(forms.Form):
    ques = forms.CharField(label = 'Question', max_length=50)
