from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import *
from django.db.models import Q
from . models import product

# Create your views here.
def home(request,c_slug=None):
    c_page=None
    obj=None
    if c_slug != None:
        c_page=get_object_or_404(category,slug=c_slug)
        obj2=product.objects.filter(cate=c_page,available=True)
    else:
        obj2=product.objects.all().filter(available=True)
    obj=category.objects.all()


    p=Paginator(obj2,4)
    page=int(request.GET.get('page', 1))

    try:
        proe=p.page(page)
    except(EmptyPage,InvalidPage):
        proe=p.page(p.num_pages)
    
    return render(request,'index.html',{'data':obj,'data2':obj2, 'pr':proe})


def single(request,id):
    obj1=get_object_or_404(product,pk=id)
    return render(request,'product-single.html',{'obj2':obj1})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def searching(request):
    if 'q' in request.GET:
        print('hai')
        query=request.GET.get('q')
        prod=product.objects.all().filter(Q(name__icontains=query)|Q(desc__icontains=query),available=True)
    if not prod:
        return HttpResponse("<script> alert('not available'):window.location='/';</script>")
    
    return render(request, "search.html", {'pr':prod})