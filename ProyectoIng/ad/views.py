from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from .models import Ad, Category, PriceRange, AdKind, Unit, Currency
from location.models import Location
from account.models import Account
from images.models import Image
from ad.forms import AdCreateForm, AdUpdateForm
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory


class ShowAdsListView(ListView):
    model= Ad
    template_name="ad_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context["ads_data"]= Ad.objects.prefetch_related().order_by('-date_created')
        return context
#id_user ,id_store ,id_location,id_ad_kind,id_category,id_unit,ad_name,ad_description,price,date_created

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'ad/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context['products']= Ad.objects.all().order_by('-date_created')
        return context

class AdDetailView(DetailView):
    model = Ad 
    template_name = 'ad/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context['ads'] = Ad.objects.all().order_by('-date_created')
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
        context['locations'] = Location.objects.filter(correlative_direction__isnull=True)
        # Fin Sidebar Context
        context['all_locations'] = Location.objects.all()
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
            ad.save()
            return HttpResponseRedirect(reverse_lazy('my_products')+'?created')
        return HttpResponseRedirect(reverse_lazy('ad_create')+'?error')

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
            ad.ad_images.clear()
            for file in request.FILES.getlist('images'):
                    instance = Image(img_route=file)
                    instance.save()
                    ad.ad_images.add(instance)
                    print(ad.ad_images)
        ad.save()
    
        

        return HttpResponseRedirect(reverse_lazy('my_products')+'?created') 
        
    
