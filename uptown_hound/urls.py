# ===============================================
# uptown_hound/urls.py
# ===============================================


from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from shop import views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/remove/$', views.cart_remove, name='cart_remove'),
    url(r'^category/search/$', views.search, name='search'),
    url(r'^category/(?P<category_path>.+)/$', views.category, name='category'),
    url(r'^checkout/thankyou/(?P<invoice_number>[\w-]+)/$',
        views.confirm_order),
    url(r'^checkout/$', views.OrderWizard.as_view(), name='checkout'),
    url(r'^order-status/$', views.order_status, name='order_status'),
    url(r'^product/(?P<product_slug>[\w-]+)/$', views.product, name='product'),
    url(r'^store/contact/$',
        TemplateView.as_view(template_name='store/contact.html')),
    url(r'^store/privacy/$',
        TemplateView.as_view(template_name='store/privacy.html')),
    url(r'^store/shipping-returns/$',
        TemplateView.as_view(template_name='store/ship_returns.html')),
    url(r'^store/terms/$',
        TemplateView.as_view(template_name='store/terms.html')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
