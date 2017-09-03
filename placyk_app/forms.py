from django import forms
from .models import Quarter, Pground, Parent, AGE, SEX, Message, Visit, Child, QUARTER
from django.core.validators import validate_email, URLValidator, ValidationError, EmailValidator
from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User
from bootstrap3_datetime.widgets import DateTimePicker


def validate_username(username):
    db_usernames = User.objects.filter(username=username)
    for db_username in db_usernames:
        if db_username == username:
            raise ValidationError('{}: taki użytkownik już istnieje!'.format(username))


class UserRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['quarter'].widget.choices = [(q.pk, q.name) for q in Quarter.objects.all()]

    username = forms.CharField(label='Użytkownik', validators=[validate_username])
    email = forms.CharField(label='e-mail', validators=[EmailValidator])
    password = forms.CharField(widget=forms.PasswordInput, label='Podaj hasło')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')
    quarter = forms.CharField(widget=forms.Select, label='Twoja dzielnica')


class ChildRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChildRegisterForm, self).__init__(*args, **kwargs)
        self.fields['age'].widget.choices = AGE
        self.fields['sex'].widget.choices = SEX

    name = forms.CharField(label='Imię')
    age = forms.IntegerField(widget=forms.Select, label='Wiek')
    sex = forms.IntegerField(widget=forms.Select, label='Płeć')


class LoginForm(forms.Form):
    email = forms.EmailField(label='e-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


class NewMessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['creation_date', 'is_read', 'sender', 'receiver']
        labels = {'content': 'Twoja wiadomość'}


class AddVisitForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        parent = Parent.objects.get(user=user)
        quarter = parent.quarter
        super(AddVisitForm, self).__init__(*args, **kwargs)
        self.fields['pground'].widget.choices = [(p.pk, p.place) for p in Pground.objects.filter(quarter=quarter)]

    pground = forms.IntegerField(widget=forms.Select, label='placyk')
    time_from = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}, attrs={'onchange': "this.form.submit()"}),
        label='od')
    time_to = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}, attrs={'onchange': "this.form.submit()"}),
        label='do')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Wprowadź nowe hasło')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Wprowadź ponownie hasło')


class EditVisitForm(ModelForm):
    class Meta:
        model = Visit
        exclude = ['who', 'pground']
        labels = {'time_from': 'Od godziny:', 'time_to': 'Do godziny:'}
        widgets = {'time_from': forms.DateTimeInput(attrs={'id': 'datetimepicker1'}),
                   'time_to': forms.DateTimeInput(attrs={'id': 'datetimepicker2'})
                   }
