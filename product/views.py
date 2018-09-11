from django.shortcuts import render
from .models import Product, Status
from .dataModels import ProductData
from user.models import User


# Create your views here.

def init_product_info(request):
    if request.method == "GET":
        # 从数据库中取出所有的产品列表
        products = Product.objects.all()
        if products.count() == 0:
            return render(request, "pages/tables.html")
        data_list = []

        # 减少数据库IO操作，在此查询所有的产品状态，并且生成一个DICT
        status_dict = {}
        for status in Status.objects.all():
            status_dict[status.id] = status.status

        # 减少数据库IO操作，因此在此查询所有的用户，并且生成一个DICT
        user_dict = {}
        for user in User.objects.all():
            user_dict[user.id] = user.name

        for product in products:
            product_name = product.name
            product_create_time = product.createTime
            product_create_user = product.createUser
            product_incharge_user = product.inChargeUser
            product_status = product.status
            product_data = ProductData(name=product_name, create_user=user_dict.get(product_create_user),
                                       incharge_user=user_dict.get(product_incharge_user),
                                       create_time=str(product_create_time),
                                       status=status_dict.get(product_status))
            data_list.append(product_data)
        else:
            return render(request, "pages/tables.html", {"products": data_list})
