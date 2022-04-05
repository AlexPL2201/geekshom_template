from django.shortcuts import render
from json import load
from mainapp.models import ProductCategories, Product
import os

# Create your views here.

def readJson():
	with open('mainapp/fixtures/content.json', 'r', encoding='utf-8') as f:
		content = load(f)
	return content


def index(request):
	return render(request, 'mainapp/index.html')


def products(request):
	categories = ProductCategories.objects.all()
	products = Product.objects.all()
	content = {
		"categories" : categories,
		"products" : products
	}
	return render(request, 'mainapp/products.html', content)