import json
from chardet import detect
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategories, Product
from authapp.models import User


def load_json(path):
	with open(path, 'rb') as f:
		contnet_bytes = f.read()
	
	detected = detect(contnet_bytes)
	encoding = detected['encoding']
	content_text = contnet_bytes.decode(encoding)
	
	with open(path, 'w', encoding='utf-8') as f:
		f.write(content_text)


	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		User.objects.create_superuser(username='Sergey', email='', password='1')
		categories = load_json('mainapp/fixtures/category.json')
		ProductCategories.objects.all().delete()

		for category in categories:
			new_category = category.get('fields')
			new_category['id'] = category.get('pk')
			ProductCategories(**new_category).save()

		products = load_json('mainapp/fixtures/product.json')
		Product.objects.all().delete()
		
		for product in products:
			new_product = product.get('fields')
			category = new_product.get('category')
			_category = ProductCategories.objects.get(id=category)
			new_product['category'] = _category
			Product(**new_product).save()
