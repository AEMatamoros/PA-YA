from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Ad, Category, PriceRange, AdKind, Unit, Currency
from location.models import Location
from account.models import Account
from images.models import Image
from ad.forms import AdCreateForm, AdUpdateForm, AdDeleteForm
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory


class UserAds(ListView):
    model= Ad
    template_name="ad/user_ad_list.html"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        uid = self.kwargs['uid']
        try:
            user = Account.objects.get(pk=self.kwargs['uid'])
        except:
            user = self.request.user
        context['user_name'] = user.get_full_name
        context['user_pk'] = user.pk
        return context
    def get_queryset(self):
        uid = self.kwargs['uid']
        try:
            user = Account.objects.get(pk=uid)
        except:
            user = self.request.user
        queryset = Ad.objects.filter(id_user__id=user.id)
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

class CategoryAds(ListView):
    model= Ad
    template_name="ad/category_ad_list.html"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        c = self.kwargs['cid']
        try:
            category = Category.objects.get(pk=c)
            context['category_name'] = category.category_name
            context['c'] = c
        except:
            context['category_name'] = "Todas las categorías"
            context['c'] = 0
        return context
    def get_queryset(self):
        cid = self.kwargs['cid']
        try:
            category = Category.objects.get(pk=cid)
            queryset = Ad.objects.filter(id_category__id=category.id)
        except:
            queryset = Ad.objects.all()
        queryset = queryset.filter(active=True).order_by('-date_created')
        return queryset

class AdDetailView(DetailView):
    model = Ad 
    template_name = 'ad/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        # Fin Sidebar Context
        return context


class CreateAd(CreateView):
    model = Ad
    form_class=AdCreateForm
    template_name= 'ad/ad_create.html' #Template al que envia el formulario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context['all_locations'] = Location.objects.all().order_by('direction')
        context['ad_kinds'] = AdKind.objects.all()
        context['units'] = Unit.objects.all()
        context['currencies'] = Currency.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = AdCreateForm(request.POST)
        if form.is_valid():
            ad= form.save(False)
            ad.id_user = request.user
            ad= form.save()
            for file in request.FILES.getlist('images'):
                instance = Image(img_route=file)
                instance.save()
                ad.ad_images.add( instance )
            if len(request.FILES.getlist('images'))==0:
                instance = Image.objects.get(pk=1)
                ad.ad_images.add( instance )
            ad.save(False)
            return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user})+'?created')
        return HttpResponseRedirect(reverse_lazy('ad_create')+'?error')


class AdDelete(UpdateView):
    model = Ad
    form_class= AdDeleteForm
    template_name = 'ad/ad_delete.html'
    context_object_name = 'Ad'
    
    def post(self, request,pk, *args, **kwargs):
        form =AdDeleteForm(request.POST)
        ad_object_data = self.object = self.get_object()
        if form.is_valid():
            ad= form.save(commit=False)
            ad= ad_object_data
            ad.active= False
            ad.save(False)
        ad.save()
        return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user})+'?deleted')
 
        


class AdUpdate(UpdateView):
    model = Ad
    form_class= AdUpdateForm
    template_name = 'ad/ad_update.html'
    context_object_name = 'Ad'
    
    def post(self, request,pk, *args, **kwargs):
        form =AdUpdateForm(request.POST)
        ad_object_data = self.object = self.get_object()

        if form.is_valid():
            ad= form.save(commit=False)
            ad.id_user = request.user
            ad.pk= ad_object_data.pk
            ad.date_created = ad_object_data.date_created
            ad.save(False)
            
            if request.FILES.getlist('images'):
                ad.ad_images.clear()

            for file in request.FILES.getlist('images'):
                    instance = Image(img_route=file)
                    instance.save()
                    ad.ad_images.add(instance)
                    
            ad.save()
    
        

        return HttpResponseRedirect(reverse_lazy('products_user',kwargs={'uid':self.request.user.id})+'?updated')
 
        
    
