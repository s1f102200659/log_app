from django import forms

class ActivityForm(forms.Form):
    activity = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 100}), label='活動内容')
    student = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}), label='生徒の様子')

class CaliculumForm(forms.Form):
     date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='日付', required=True)
     objective = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='本日のねらい', required=True)

class SendedForm(forms.Form):
    sheet = forms.CharField(widget=forms.HiddenInput())
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2, 
            'style': 'width: 100%; font-size: large;'
        }),
        label='メッセージ',
        required=True
    )