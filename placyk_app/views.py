from django.shortcuts import render
from .models import User, Parent, AGE, Pground, Visit, Quarter, QUARTER, Message, Child
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.template.response import TemplateResponse
from .forms import UserRegisterForm, ChildRegisterForm, NewMessageForm, LoginForm, AddVisitForm, \
    ResetPasswordForm, EditVisitForm
from django .http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from datetime import datetime
# from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home')
        quarters = Quarter.objects.all().order_by('name')
        pgrounds = {}
        for quarter in quarters:
            pgrounds[quarter] = quarter.pground_set.all()
        ctx = {'pgrounds': pgrounds}
        return TemplateResponse(request, 'home.html', ctx)


class HomeLogView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        user = request.user
        quarter = user.parent.quarter
        pgrounds = quarter.pground_set.all()
        current_visits = {}
        for pground in pgrounds:
            now = datetime.now()
            current_visits[pground] = pground.visit_set.filter(time_from__lte=now, time_to__gte=now)
            current_visits[pground] = {}
            this_visits = pground.visit_set.filter(time_from__lte=now, time_to__gte=now)
            for visit in this_visits:
                current_visits[pground][visit] = Child.objects.filter(whose_child=visit.who)

        ctx = {'user': user, 'quarter': quarter, 'pgrounds': pgrounds, 'current_visits': current_visits, 'this_visits': this_visits}
        return TemplateResponse(request, 'home_login.html', ctx)



class UserRegisterView(View):

    def get(self, request):
        form = UserRegisterForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'register.html', ctx)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                quarter_id = form.cleaned_data['quarter']
                user = User.objects.create_user(username=username, email=email, password=password)
                parent = Parent.objects.create(user=user, quarter_id=quarter_id)
                if user is not None:
                   login(request, user)
                   return HttpResponseRedirect('/register_child/' + str(user.id))
                else:
                    ctx = {'msg': 'Wystąpił błąd, nie jesteś zalogowany'}
                    return TemplateResponse(request, 'register.html', ctx)
            else:
                raise ValidationError("Hasła się różnią!")
        else:
            ctx = {"form": form, 'msg': 'Nieprawidłowe dane!'}
            return TemplateResponse(request, 'register.html', ctx)


class ChildRegisterView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = ChildRegisterForm()
        ctx = {'form': form, 'user': user}
        return TemplateResponse(request, 'register_child.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = ChildRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            child = Child.objects.create(name=name, age=age, sex=sex, whose_child=user)
            if request.POST['submit'] == 'add':
                user = User.objects.get(id=id)
                form = ChildRegisterForm()
                ctx = {'form': form, 'user': user}
                return TemplateResponse(request, 'register_child.html', ctx)
            else:
                user = User.objects.get(id=id)
                return HttpResponseRedirect('/home')
        else:
            ctx = {"form": form, 'msg': 'Nieprawidłowe dane!'}
            return TemplateResponse(request, 'register_child.html', ctx)


class LoginView(View):

    def get(self, request):
        form = LoginForm
        ctx = {'form': form}
        return TemplateResponse(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home_login')
            else:
                ctx = {'msg': 'Nieprawidłowe dane!'}
                return TemplateResponse(request, 'login.html')
        else:
            ctx = {'msg': 'Nieprawidłowe dane!'}
            return TemplateResponse(request, 'login.html')



class LogoutView(View):

    def get(self, request, id):
        logout(request)
        ctx = {'msg': 'Zostałeś wylogowany'}
        return TemplateResponse(request, 'logout.html', ctx)


class NewMessageView(LoginRequiredMixin, View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm()
        ctx = {'form': form, 'user': user}
        return TemplateResponse(request, 'new_message.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            receiver = user
            content = form.cleaned_data['content']
            if sender == receiver:
                ctx = {'msg': 'Wysyłasz wiadmość do samego siebie!'}
                return TemplateResponse(request, 'new_message.html', ctx)
            else:
                message = Message(sender=sender, receiver=receiver, content=content)
                message.save()
                ctx = {'msg': 'Wysłałeś wiadomość!', 'user': user}
                return HttpResponseRedirect('/home')
        else:
            ctx = {'form': form, 'user': user}
            return TemplateResponse(request, 'new_message.html', ctx)


class MessageView(LoginRequiredMixin, View):

    def get(self, request, id):
        message = Message.objects.get(id=id)
        if message.receiver == self.request.user:
            message.is_read = True
            message.save()
        ctx = {'message': message}
        return TemplateResponse(request, 'details_message.html', ctx)


class UserMessagesView(LoginRequiredMixin, View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        messages_sent = Message.objects.filter(sender=user).order_by('-creation_date')[:20]
        messages_received = Message.objects.filter(receiver=user).order_by('-creation_date')[:20]
        ctx = {'user': user, 'messages_sent': messages_sent, 'messages_received': messages_received}
        return TemplateResponse(request, 'user_messages.html', ctx)


class AddVisitView(LoginRequiredMixin, View):


    def get(self, request, id):
        user = User.objects.get(id=id)
        form = AddVisitForm(user=user)
        ctx = {'form': form, 'user': user}
        return TemplateResponse(request, 'add_visit.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = AddVisitForm(user, request.POST)
        now = datetime.now()
        if form.is_valid():
            pground_id = form.cleaned_data['pground']
            time_from = form.cleaned_data['time_from']
            time_to = form.cleaned_data['time_to']
            if time_to <= time_from:
                ctx = {'form': form, 'user': user}
                messages.error(request, 'Termin końca pobytu nie może być wcześnieszy niż początku!')
                return TemplateResponse(request, 'add_visit.html', ctx)
            elif time_to <= now:
                ctx = {'form': form, 'user': user}
                messages.error(request, 'Termin, który próbujesz ustalić już minął!')
                return TemplateResponse(request, 'add_visit.html', ctx)
            else:
                visit = Visit.objects.create(pground_id = pground_id, time_from=time_from, time_to=time_to, who=user)
                ctx = {'user': user}
                messages.success(request, 'Dodałeś informację!')
                return TemplateResponse(request, 'add_visit.html', ctx)
        else:
            ctx = {'form': form, 'user': user}
            return TemplateResponse(request, 'add_visit.html', ctx)


class UserView(LoginRequiredMixin, View):

    def get(self, request, id):
        user = User.objects.get(id=int(id))
        now = datetime.now()
        visits = Visit.objects.filter(who=user).filter(time_to__gte=now).order_by('time_from')
        ctx = {'user': user, 'visits': visits}
        return TemplateResponse(request, 'user_site.html', ctx)


class DeleteVisitView(LoginRequiredMixin, View):

    def get(self, request, id):
        visit = Visit.objects.get(id=id)
        visit.delete()
        ctx = {'msg': 'Wizyta została skasowana'}
        return TemplateResponse(request, 'delete_visit.html', ctx)


class ResetPasswordView(LoginRequiredMixin, View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = ResetPasswordForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'reset_password.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                ctx={'msg': 'Hasła są różne!'}
                return TemplateResponse(request, 'reset_password.html', ctx)
            else:
                user.set_password(form.cleaned_data['password'])
                user.save()
                ctx = {'msg': 'Hasło zostało zmienione!'}
                return HttpResponseRedirect('/home')


class EditVisitView(View):

    def get(self, request, id):
        visit = Visit.objects.get(id=id)
        form = EditVisitForm(instance=visit)
        ctx = {'form': form, 'visit': visit, 'id': id}
        return TemplateResponse(request, 'edit_visit.html', ctx)

    def post(self, request, id):
        visit = Visit.objects.get(id=id)
        p = Visit.objects.get(id=id)
        form = EditVisitForm(request.POST, instance=p)
        ctx = {'form': form}
        if form.is_valid():
            form.save()
            ctx = {'msg': 'Zmieniłeś czas pobytu na placyku!', 'visit': visit}
            return TemplateResponse(request, 'edit_visit.html', ctx)
        else:
            ctx = {'form': form, 'visit': visit, 'id': id}
            return TemplateResponse(request, 'edit_visit.html', ctx)



