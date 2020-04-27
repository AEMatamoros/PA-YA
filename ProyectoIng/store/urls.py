from django.urls import path
from .views import CreateStore, UserStores, StoreDetailView, StoreUpdate, StoreDelete, CreateAdStore, update_store, deleteAd

urlpatterns = [
    path('create',CreateStore.as_view(), name='create_store'),
    path('user/<uid>',UserStores.as_view(), name='user_stores'),
    path('store/<int:pk>', StoreDetailView.as_view(), name="store_detail"),
    #path('<int:pk>/update', StoreUpdate.as_view(), name='update_store'),
    path('<int:pk>/delete', StoreDelete.as_view(), name = 'delete_store'),
    path('store/update', update_store, name="up_store"),
    path('store/createAd', CreateAdStore.as_view(), name="ad_create_store"),
    path('store/deleteAd', deleteAd, name="ad_delete"),
]