from django.shortcuts import render
from product.models import Product
from product import views as pViews


# Create your views here.



def init_upload_page(request):
    if request.method == "GET":
        # 从session中获取当前登录的用户
        name = request.session.get("user")
        # 获取所有的产品列表，然后传回并且生成select列表
        product_query_set = Product.objects.all()
        products = [product.name for product in product_query_set]
        # 获取第一个产品的相关详细信息，并且传递到前端页面
        first_product = pViews.product_detail_no_request(products[0])
        return render(request, "pages/testcase/upload.html",
                      {"user": name, "products": products, "relatedData": first_product})
    if request.method == "POST":
        pass
