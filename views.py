from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import Commodity, UInfo
from .forms import UInfoForm, UserForm, CommodityForm

# Create your views here.

class IndexView(ListView):
    template_name = 'market/index.html'
    context_object_name = 'commodites_list'
    model = Commodity

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['home'] = True
        return context

    def get_queryset(self):
        return Commodity.objects.all()

@csrf_protect
def Register(request):
    # 用户注册
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('market:index'))
    if request.method == 'POST':
        uform = UserForm(request.POST, instance=User())
        uinfo = UInfoForm(request.POST, request.FILES, instance=UInfo())
        if uform.is_valid() and uinfo.is_valid:
            u = uform.save(commit=False)
            u.set_password(u.password)
            u.save()
            uinfo = uinfo.save(commit=False)
            uinfo.user = u
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
    # 修改用户资料
    if request.method == 'POST':
        form =  UInfoForm(request.POST, request.FILES,instance=request.user.uinfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('market:index'))
    else:
        form = UInfoForm(instance=request.user.uinfo)

    return render(request, 'market/info_modify.html', {
        'form': form,
    })


@csrf_protect
@login_required(login_url='market:login')
def CommodityAdd(request):
    # 发布物品
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES, instance=Commodity())
        if form.is_valid:
            commodity =  form.save(commit=False)
            commodity.user = request.user
            commodity.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('market:index'))
    else:
        form = CommodityForm(initial={
            'available': True
        } ,instance = Commodity())

    return render(request, 'market/commodity_add.html', {
        'form': form,
    });

class CommodityView(DetailView):
    # 展示物品
    model = Commodity
    context_object_name = 'commodity'
    template_name = 'market/commodity_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # 只有自己才可编辑自己的商品
        if self.request.user.is_authenticated and self.request.user == self.object.user:
            context['editable'] = True
        return context

