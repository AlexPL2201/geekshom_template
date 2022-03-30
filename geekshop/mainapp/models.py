from django.db import models

# Create your models here.

class ProductCategories(models.Model):
	name = models.CharField(max_length=64, unique=True)
	description = models.TextField(blank=True, null=True)

	
	def __str__(self):
		return self.name

	
	def getCategories(self):
		categoryList = []
		for category in self.objects.all():
			categoryList.append({"name" : category.name})
		return categoryList


class Product(models.Model):
	name = models.CharField(max_length=128)
	image = models.ImageField(upload_to='products_images', blank=True)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	quantity = models.PositiveIntegerField(default=0)
	category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)

	
	def __str__(self):
		return f'{self.name} | {self.category} | {self.price}' 


	def getProducts(self):
		productList = []
		for product in self.objects.all():
			productList.append({"name" : product.name, "price" : product.price, "description" : product.description, "image" : product.image})
		return productList