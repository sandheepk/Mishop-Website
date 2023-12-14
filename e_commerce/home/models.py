from django.db import models
from django.urls import reverse

# Create your models here.

class category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=50, unique=True)


    def __str__(self):
        return '{}' .format(self.name)
    
    def get_url(self):
        return reverse('prod_cat',args=[self.slug])


class product(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50, unique=True)
    img=models.ImageField(upload_to='product')      
    cate=models.ForeignKey(category, on_delete=models.CASCADE)
    desc=models.TextField()
    date=models.DateField()
    stock=models.IntegerField(max_length=50)
    price=models.IntegerField()
    available=models.BooleanField()


    def __str__(self):
        return '{}' .format(self.name)
    

