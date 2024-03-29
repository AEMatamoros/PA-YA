from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.db import models
from django.db.models import Value, Case, When, F, OuterRef, Subquery, Avg
from django.db.models.functions import Concat
from scrape.models import Exchange
from ad.models import Ad, Category, PriceRange, Currency, AdKind
from location.models import Location
from account.models import Account
from store.models import Store
from images.models import Image
from rating.models import Rating
from .models import Search

class SearchView(ListView):
    template_name="search/search.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar Context
        context['categories'] = Category.objects.order_by('category_name')
        context['price_ranges'] = PriceRange.objects.all()
        context['locations'] = Location.objects.order_by('direction').filter(correlative_direction__isnull=True)
        context['currencies'] = Currency.objects.all()
        context['ad_kinds'] = AdKind.objects.all()
        # Fin Sidebar Context
        q = self.request.GET.get("search_q")
        if q is None:
            q=""
        currency = self.request.GET.get("search_currency")
        if currency is None:
            currency=1
        try:
            min_price = float(self.request.GET.get("search_min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("search_max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("search_c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("search_l"))
        except:
            l = 0
        try:
            r = int(self.request.GET.get("search_r"))
        except:
            r = 0
        try:
            category_name = Category.objects.get(pk=c).category_name
        except:
            category_name = "Todas las categorías"
        try:
            location_name = str(Location.objects.get(pk=l))
        except:
            location_name = "Todo lugar"
        if c == -1:
            context['ad_search'] = False
            context['user_search'] = True
            context['store_search'] = False
        elif c == -2:
            context['ad_search'] = False
            context['user_search'] = False
            context['store_search'] = True
        else:
            context['ad_search'] = True
            context['user_search'] = False
            context['store_search'] = False
        context['search_q'] = q
        context['search_currency'] = currency
        context['search_min'] = min_price
        context['search_max'] = max_price
        context['search_c'] = c
        context['search_l'] = l
        context['search_r'] = r
        context['search_category_name'] = category_name
        context['search_location_name'] = location_name
        context['default_image'] = Image.objects.get(pk=1)
        return context

    def get_queryset(self):
        search = Search()
        if self.request.user.is_authenticated:
            search.id_user = self.request.user
        q = self.request.GET.get("search_q")
        if q is None:
            q=""
        search.query_search = q
        try:
            min_price = float(self.request.GET.get("search_min"))
        except:
            min_price = 0
        try:
            max_price = float(self.request.GET.get("search_max"))
        except:
            max_price = 0
        try:
            c = int(self.request.GET.get("search_c"))
        except:
            c = 0
        try:
            l = int(self.request.GET.get("search_l"))
        except:
            l = 0
        try:
            r = int(self.request.GET.get("search_r"))
        except:
            r = 0
        search.min_rating = r
        try:
            currency = int(self.request.GET.get("search_currency"))
        except:
            currency = 1
        if c == -1:
            #Busqueda de usuarios
            search.user_search = True
            queryset = Account.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'),
                publisher_rating = Subquery(
                    Rating.objects.filter(evaluated_user=OuterRef('pk'), evaluated_store__isnull = True)
                    .annotate(rating=Avg('points')).values('rating')[:1])
            )
            queryset = queryset.filter(publisher_rating__gte=(r)) | queryset.filter(publisher_rating=None)
            queryset = queryset.filter(full_name__icontains=q) | queryset.filter(email__icontains=q)
            try:
                location = Location.objects.get(pk=l)
            except:
                location = None
            #Filtro de lugar
            if location is not None:
                queryset = queryset.filter(location__pk=l) | queryset.filter(location__correlative_direction__pk=l)
                search.id_location = location
            search.save()
            return queryset
        elif c == -2:
            #Busqueda de tiendas
            search.store_search = True
            queryset = Store.objects.filter(active=True)
            queryset = queryset.annotate(publisher_rating = Subquery(
                    Rating.objects.filter(evaluated_store=OuterRef('pk'), evaluated_user__isnull = True)
                    .annotate(rating=Avg('points')).values('rating')[:1]
                    )
            )
            queryset = queryset.filter(publisher_rating__gte=(r)) | queryset.filter(publisher_rating=None)
            queryset = queryset.filter(store_name__icontains=q) | queryset.filter(store_description__icontains=q)
            try:
                location = Location.objects.get(pk=l)
            except:
                location = None
            #Filtro de lugar
            if location is not None:
                queryset = queryset.filter(store_location__pk=l) | queryset.filter(store_location__correlative_direction__pk=l)
                search.id_location = location
            #queryset = queryset.order_by('-date_created')
            search.save()
            return queryset
        else:
            exchange = Exchange.objects.get(pk=1)
            user_ratings = Rating.objects.filter(evaluated_user__isnull=False, evaluated_user=OuterRef('id_user'))
            store_ratings = Rating.objects.filter(evaluated_store__isnull=False, evaluated_store=OuterRef('id_store'))
            #Busqueda de anuncios
            search.ad_search = True
            #Validacion de minimo y maximo
            #Si solo se selecciono precio minimo, el precio maximo viene con valor 0
            #Si solo se selecciono precio maximo, el precio minimo viene con valor 0
            #Si no se selecciono minimo ni maximo, ambos vienen con valor 0
            if  (min_price > max_price and max_price != 0):
                temp = max_price
                max_price = min_price
                min_price = temp
            #Filtro de precios
            #Precio original en lempiras
            search.set_id_price_range(min_price, max_price, None)
            queryset = Ad.objects.annotate(
                price_lempiras=Case(
                    When(id_currency__pk = 1, then = F('price')),
                    When(id_currency__pk = 2, then = F('price')*exchange.exchange),
                    output_field=models.FloatField(),
                ),
                price_dollar=Case(
                    When(id_currency__pk = 2, then = F('price')),
                    When(id_currency__pk = 1, then = F('price')/exchange.exchange),
                    output_field=models.FloatField(),
                ),
            )
            #Annotate publisher rating
            queryset = queryset.publisher_rating()
            #Filtro por rating (Los que no han sido evaluados siempre se muestran)
            queryset = queryset.filter(publisher_rating__gte=(r)) | queryset.filter(publisher_rating=None)
            if currency == 1:
                queryset = queryset.filter(price_lempiras__gte=(min_price))
                if (max_price != 0):
                    #Se selecciono un precio maximo
                    queryset = queryset.filter(price_lempiras__lte=(max_price))
            else:
                queryset = queryset.filter(price_dollar__gte=(min_price))
                if (max_price != 0):
                    #Se selecciono un precio maximo
                    queryset = queryset.filter(price_dollar__lte=(max_price))
            #Validacion de categorias
            try:
                category = Category.objects.get(pk=c)
            except:
                category = None
            #Filtro de categorias
            if category is not None:
                queryset = queryset.filter(id_category__pk=c)
                search.id_category = category
            #Validacion de lugar
            try:
                location = Location.objects.get(pk=l)
            except:
                location = None
            #Filtro de lugar
            if location is not None:
                queryset = queryset.filter(id_location__pk=l) | queryset.filter(id_location__correlative_direction__pk=l)
                search.id_location = location
            #Filtro de nombre o descripcion
            queryset = queryset.filter(ad_name__icontains=q) | queryset.filter(ad_description__icontains=q)
            queryset = queryset.filter(active=True).order_by('-date_created')
            search.save()
            return queryset
