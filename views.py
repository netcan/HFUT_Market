from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import Commodity, UInfo, Category, Tag
from .forms import UInfoForm, UserForm, CommodityForm

# Create your views here.

class IndexView(ListView):
    template_name = 'market/index.html'
    context_object_name = 'commodites_list'
    model = Commodity

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['home'] = True
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        if self.request.GET.get('category'):
            context['selected'] = self.request.GET.get('category')
            context['count'] = get_object_or_404(Category, name=context['selected']).commodity_set.count()
            context['parm'] = 'category=' + context['selected']
        elif self.request.GET.get('tag'):
            context['selected'] = self.request.GET.get('tag')
            context['count'] = get_object_or_404(Tag, name=context['selected']).commodity_set.count()
            context['parm'] = 'tag=' + context['selected']
        elif self.request.GET.get('search'):
            context['parm'] = 'search=' + self.request.GET.get('search')
        elif 'mypublish' in self.request.GET:
            context['parm'] = 'mypublish'
            if self.request.user.is_authenticated == False:
                context['message'] = '请先登录。'

        return context

    def get_queryset(self):
        qs = Commodity.objects.filter(available=True).order_by('-date')
        if self.request.GET.get('category'):
            qs = qs.filter(category__name = self.request.GET.get('category'))
        elif self.request.GET.get('tag'):
            qs = qs.filter(tags__name = self.request.GET.get('tag'))
        elif self.request.GET.get('search'):
            search = self.request.GET.get('search')
            qs = qs.filter(Q(name__icontains=search) | Q(introduction__icontains=search) | Q(user__username__icontains=search))
        elif 'mypublish' in self.request.GET:
            if self.request.user.is_authenticated == False:
                return None

            qs = Commodity.objects.filter(user=self.request.user).order_by('-date')

        # 分页
        paginator = Paginator(qs, 8) # 每页8个商品
        page = self.request.GET.get('page')
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        return qs

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
def InfoEdit(request):
    # 修改用户资料
    if request.method == 'POST':
        form =  UInfoForm(request.POST, request.FILES,instance=request.user.uinfo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('market:index'))
    else:
        form = UInfoForm(instance=request.user.uinfo)

    return render(request, 'market/info_edit.html', {
        'form': form,
    })


@csrf_protect
@login_required(login_url='market:login')
def CommodityAdd(request):
    # 发布物品
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES, instance=Commodity())
        if form.is_valid():
            commodity =  form.save(commit=False)
            commodity.user = request.user
            commodity.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('market:index') + '?mypublish')
    else:
        form = CommodityForm(initial={
            'available': True
        } ,instance = Commodity())

    return render(request, 'market/commodity_add_or_edit.html', {
        'form': form,
        'action': '发布物品',
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

@csrf_protect
@login_required(login_url='market:login')
def CommodityEdit(request, pk):
    # 修改物品
    commodity = get_object_or_404(Commodity, pk=pk)
    if commodity.user != request.user:
        return HttpResponseNotAllowed(['GET', 'POST'])

    if(request.method == 'POST'):
        if request.POST.get('commodityToggle'):
            commodity.available = not commodity.available
            commodity.save()
            return HttpResponseRedirect(request.POST.get('next'))

        form = CommodityForm(request.POST, request.FILES, instance=commodity)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('market:commodity_view', kwargs={'pk': pk}))
    else:
        form = CommodityForm(instance = commodity)
    return render(request, 'market/commodity_add_or_edit.html', {
        'form': form,
        'action': '修改物品',
    });

@csrf_protect
@login_required(login_url='market:login')
def CommodityDelete(request, pk):
    # 删除物品
    commodity = get_object_or_404(Commodity, pk=pk)
    if commodity.user != request.user:
        return HttpResponseNotAllowed(['GET', 'POST'])

    if request.method == 'POST':
        commodity.delete()
        return HttpResponseRedirect(reverse('market:index'))
    else:
        return HttpResponseNotAllowed(['GET'])



