from django.shortcuts import render
from product.models import Product


# Create your views here.



def init_upload_page(request):
    if request.method == "GET":
        # 从session中获取当前登录的用户
        name = request.session.get("user")
        # 获取所有的产品列表，然后传回并且生成select列表
        product_query_set = Product.objects.all()
        products = [product.name for product in product_query_set]
        print(products)
        return render(request, "pages/testcase/upload.html", {"user": name, "products": products})
    if request.method == "POST":
        pass
