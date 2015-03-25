from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from shop import views


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/remove/$', views.cart_remove, name='cart_remove'),
    url(r'^category/(?P<cat_slugs>.+)/$', views.category, name='category'),
    url(r'^product/(?P<product_slug>[\w-]+)/$', views.product, name='product'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
