from django import forms
from .models import Comment

class TicketForm(forms.Form):

    SUBJECT_CHOICES = [
        ('account','مشکل حساب کاربری'),
        ('payment', 'مشکل پرداخت'),
        ('bug', 'گزارش باگ'),
        ('suggestion', 'پیشنهاد'),
        ('other', 'سایر موارد')
    ]

    message = forms.CharField(widget=forms.Textarea,required=True)
    name = forms.CharField(max_length=250,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11,required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name' , 'body']

#search
class SearchForm(forms.Form):
    query = forms.CharField()