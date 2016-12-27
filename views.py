from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from .models import Commodity, UInfo
from .forms import RegisterForm

# Create your views here.

class IndexView(ListView):
    template_name = 'market/index.html'
    context_object_name = 'latest_commodites_list'
    model = Commodity

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['home'] = True
        return context

@csrf_protect
def Register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('market:index'))
    errors = None
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
             if(request.POST['password'] != request.POST['password2']):
                 errors = "密码不一致"
             else:
                 avatar = request.FILES['avatar']
                 if avatar:
                    fs = FileSystemStorage(location='uploads/avatar')
                    avatarName = fs.save(avatar.name, avatar)
                 u = User(username = request.POST['username'],
                          email = request.POST['email'])
                 u.set_password(request.POST['password'])
                 u.save()

                 uinfo = UInfo(avatar = 'uploads/avatar' + fs.url(avatarName) if fs else None,
                               qq = request.POST['qq'] if request.POST['qq'] else None,
                               phone = request.POST['phone'] if request.POST['phone'] else None,
                               )
                 uinfo.user = u
                 uinfo.save()
                 return HttpResponseRedirect(reverse('market:login') + '?next=' + reverse('market:index'))
    else:
        form = RegisterForm

    return render(request, 'market/register.html', {
        'form': form,
        'errors': errors
    })
