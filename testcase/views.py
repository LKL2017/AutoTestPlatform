from django.shortcuts import render
from product.models import Product
from product import views as pViews
from testcase.models import TestCase, CaseModule
from user.userUtils import user_dict
from testcase.dataModels import TestCaseData, TestCaseDetail


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


def init_case_list(request):
    """初始化测试用例列表页面的显示方式"""
    if request.method == "GET":
        """
        当请求方式为GET时，初始化测试用例页面的显示，该页面为/pages/testcase/list.html
        首先请求用例模组，然后根据用例模组初始化用例列表
        """
        module_queryset = CaseModule.objects.all()
        module_dict = dict(
            [(m.id, m) for m in module_queryset]
        )
        users_dict = user_dict()
        # 请求用例列表
        case_queryset = TestCase.objects.all()
        first_case = ""
        # 根据用例列表来进行分组，生成DICT
        module_case_dict = {}
        for _id in module_dict.keys():
            case_list = [case.title for case in case_queryset if case.case_module == _id]
            if first_case == "" and len(case_list) != 0:
                first_case = case_list[0]
            module_case_dict[module_dict.get(_id).name] = case_list
        # 获取一个待显示的Case信息
        first_case = case_queryset.filter(title=first_case)[0]
        # 传输数据说明：
        # module_case_list：NAME:LIST
        # user_dict：用户ID:NAME 字典
        # first_case：第一个需要显示的case
        first_case_detail = TestCaseDetail(first_case)
        first_case = TestCaseData(first_case, users_dict, module_dict)

        return render(request, "pages/testcase/list.html",
                      {"module_case_dict": module_case_dict, "first_case": first_case,
                       "first_case_detail": first_case_detail
                       })
