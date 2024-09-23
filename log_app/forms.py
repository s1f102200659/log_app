from django import forms

class ActivityForm(forms.Form):
    activity = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 100}), label='活動内容')
    student = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}), label='生徒の様子')
