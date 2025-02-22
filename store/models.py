from django.db import models
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, unique=True)

    class Meta:

        verbose_name_plural = 'categories'

    def __str__(self):

        return self.name
    

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

    
class Product(models.Model): 
    
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=4, decimal_places=2)

    image = models.ImageField(upload_to='images/')

    order = models.IntegerField(default=0)

    quantity = models.IntegerField(default=0)  # Default to 0 or a positive number if you want initial stock


    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):

        return self.title


    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    @property
    def in_stock(self):
        """
        Property to check if the product is in stock based on quantity.
        """
        return self.quantity > 0

    def stock_status(self):
        """
        Method to return the stock status of the product.
        """
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= 3:
            return f"{self.quantity} left"
        else:
            return "In Stock"