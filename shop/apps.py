# ===============================================
# shop/apps.py
# ===============================================


from django.apps import AppConfig
import watson


class ShopConfig(AppConfig):
    """
    Extend AppConfig to register models to be included in Watson search
    """
    name = 'shop'
    
    def ready(self):
        Product = self.get_model('Product')
        watson.register(
            Product.objects.filter(active=True), fields=('description', 'name',)
        )
