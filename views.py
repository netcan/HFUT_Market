from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from .models import Commodity, UInfo
from .forms import UInfoForm, UserForm

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
    # 用户注册
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('market:index'))
    if request.method == 'POST':
        uform = UserForm(request.POST, instance=User())
        uinfo = UInfoForm(request.POST, instance=UInfo())
        if uform.is_valid() and uinfo.is_valid:
            avatar = request.FILES['avatar']
            if avatar:
                fs = FileSystemStorage(location='uploads/avatar')
                avatarName = fs.save(avatar.name, avatar)

            u = uform.save(commit=False)
            u.set_password(u.password)
            u.save()
            uinfo = uinfo.save(commit=False)
            uinfo.user = u
            uinfo.avatar = 'uploads/avatar' + fs.url(avatarName) if fs else None

            uinfo.save()
            return HttpResponseRedirect(reverse('market:login') + '?next=' + reverse('market:index'))
    else:
        uform = UserForm(instance=User())
        uinfo = UInfoForm(instance=UInfo())

    return render(request, 'market/register.html', {
        'uform': uform,
        'uinfo': uinfo,
    })

@csrf_protect
@login_required(login_url='market:login')
def InfoModify(request):
    if request.method == 'POST':
        form =  UInfoForm(request.POST, instance=request.user.uinfo)
        if form.is_valid():
            uinfo = form.save(commit=False)
            avatar = request.FILES['avatar'] if 'avatar' in request.FILES else None
            if avatar:
                fs = FileSystemStorage(location='uploads/avatar')
                avatarName = fs.save(avatar.name, avatar)
                uinfo.avatar = 'uploads/avatar' + fs.url(avatarName) if fs else None

            uinfo.save()
            return HttpResponseRedirect(reverse('market:index'))
    else:
        form = UInfoForm(instance=request.user.uinfo)

    return render(request, 'market/info_modify.html', {
        'form': form,
    })


