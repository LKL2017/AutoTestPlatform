from django.http import JsonResponse
from django.shortcuts import render

from user.models import User
from .dataModels import ProductData, ProductRelatedData
from .models import Product, Status


# Create your views here.

def init_product_info(request):
    """
    视图方法：用于初始化产品信息页面
    仅可使用GET进行请求
    """

    if request.method == "GET":
        # 从数据库中取出所有的产品列表
        products = Product.objects.all()
        if products.count() == 0:
            return render(request, "pages/product/productList.html")
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
            product_data = ProductData(product.id, name=product_name, create_user=user_dict.get(product_create_user),
                                       incharge_user=user_dict.get(product_incharge_user),
                                       create_time=str(product_create_time),
                                       status=status_dict.get(product_status), manager=product.manager,
                                       desc=product.desc)
            data_list.append(product_data)
        else:
            return render(request, "pages/product/productList.html", {"products": data_list})


def product_detail(request, name=None):
    """用于显示产品详情视图"""
    """获取所有页面展示的信息，需要查询用户、产品和权限表"""
    if request.method == "POST":
        name = request.POST.get("name")
    product = Product.objects.filter(name=name)[0]
    create_user_name = User.objects.filter(id=product.createUser)[0].name
    incharge_user = User.objects.filter(id=product.inChargeUser)[0].name
    status = Status.objects.filter(id=product.status)[0].status
    relatedData = ProductRelatedData(product.id, name, create_user_name, incharge_user, product.createTime, status,
                                     product.manager, product.desc)
    # TODO 需要添加产品相关的统计数据
    relatedData.privileges = None
    relatedData.task_count = 0
    relatedData.test_case_count = 0

    if request.method == "GET":
        return render(request, "pages/product/detail.html", {"relatedData": relatedData})
    if request.method == "POST":
        return JsonResponse(relatedData.__dict__)


def product_detail_no_request(name=None):
    """用于获取产品的相关信息并且返回"""
    product = Product.objects.filter(name=name)[0]
    create_user_name = User.objects.filter(id=product.createUser)[0].name
    incharge_user = User.objects.filter(id=product.inChargeUser)[0].name
    status = Status.objects.filter(id=product.status)[0].status
    relatedData = ProductRelatedData(product.id, name, create_user_name, incharge_user, product.createTime, status,
                                     product.manager, product.desc)
    # TODO 需要添加产品相关的统计数据
    relatedData.privileges = None
    relatedData.task_count = 0
    relatedData.test_case_count = 0
    return relatedData
