from django.db import models
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in EUR (€)")
    image = CloudinaryField('image', folder="Ingrid/Products/")
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    pdf_link = models.URLField(blank=True, null=True, help_text="Public Google Drive link to product PDF")

    def __str__(self):
        return self.name

    def get_price(self):
        """ Returns sale price if applicable, otherwise the regular price """
        return self.sale_price if self.is_on_sale and self.sale_price else self.price

    def get_price_display(self):
        """Formats the price with the Euro (€) symbol."""
        return f"€{self.get_price():,.2f}"