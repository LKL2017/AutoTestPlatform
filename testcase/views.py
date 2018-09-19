from django.shortcuts import render, redirect
from product.models import Product
from product import views as pViews
from testcase.models import TestCase, CaseModule
from user.userUtils import user_dict
from testcase.dataModels import TestCaseData, TestCaseDetail
from django.http import JsonResponse
from AutoTestPlatform.CommonModels import ResultEnum, SqlResultData, result_to_json
import json

# Create your views here.


current_case_id = "current_case_id"


def module_dict():
    """
    :return: 模组的ID：模组的对应表
    """
    modules = CaseModule.objects.all()
    return dict([
        (mod.id, mod) for mod in modules
    ])


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
            case_list = [case for case in case_queryset if case.case_module == _id]
            if first_case == "" and len(case_list) != 0:
                first_case = case_list[0]
            module_case_dict[module_dict.get(_id).name] = case_list
        # 获取一个待显示的Case信息
        first_case = case_queryset.filter(id=first_case.id)[0]
        # 传输数据说明：
        # module_case_list：NAME:LIST
        # user_dict：用户ID:NAME 字典
        # first_case：第一个需要显示的case
        # 将当前操作的测试用例ID写入到session
        request.session[current_case_id] = first_case.id
        first_case_detail = TestCaseDetail(first_case)
        first_case = TestCaseData(first_case, users_dict, module_dict)

        return render(request, "pages/testcase/list.html",
                      {"module_case_dict": module_case_dict, "first_case": first_case,
                       "first_case_detail": first_case_detail
                       })


def case_data(request):
    """用于异步请求测试用例的数据"""
    """请求需要测试用例的ID"""
    if request.method == "GET":
        case_id = request.GET.get("id")
        case = TestCase.objects.filter(id=case_id)
        if len(case) == 0:
            return
        case = case[0]
        caseData = TestCaseData(case, user_dict(), module_dict())
        caseData_dict = caseData.__dict__
        caseData_dict.pop("_state")
        data = {"caseData": caseData_dict}
        caseDetail = TestCaseDetail(case)
        data["caseDetail"] = caseDetail.__dict__
        # 将当前操作的测试用例ID写入到session
        request.session[current_case_id] = case.id
        # 返回数据
        return JsonResponse(data)
    if request.method == "POST":
        """此处进行测试用例的删除"""
        caseData = request.POST.get("caseData")
        updateType = int(request.POST.get("type"))
        _case = TestCase.objects.filter(id=request.session[current_case_id])[0]
        caseData = json.loads(caseData)
        print(caseData)
        if updateType == 1:
            # 更新title
            _case.title = caseData["title"]
        if updateType == 2:
            # 更新前置条件
            pres = caseData["pres"]
            pres_string = " "
            pres_string = pres_string.join(pres)
            print(pres_string)
            _case.precondition = pres_string
        if updateType == 3:
            # 修改步骤和期望
            steps = caseData["steps"]
            expects = caseData.expects
            step_string = " ".join(steps)
            expects_string = " ".join(expects)
            _case.steps = step_string
            _case.expect = expects_string
        try:
            print(_case.__dict__)
            _case.save()
        except ValueError as error:
            result = SqlResultData(ResultEnum.Error, error)
            return JsonResponse(result_to_json(result))
        else:
            result = SqlResultData(ResultEnum.Success)
            return JsonResponse(result_to_json(result))


def init_case_detail(request):
    """初始化测试用例详情页面"""
    if request.method == "GET":
        """
        当请求方式为GET时，初始化测试用例页面的显示，该页面为/pages/testcase/modCase.html
        """
        users_dict = user_dict()
        # 请求用例列表
        first_case = TestCase.objects.filter(id=request.session[current_case_id])[0]
        # 传输数据说明：
        # module_case_list：NAME:LIST
        # user_dict：用户ID:NAME 字典
        # first_case：第一个需要显示的case
        # 将当前操作的测试用例ID写入到session
        request.session["current_case"] = first_case.id
        first_case_detail = TestCaseDetail(first_case)
        print("detail=" + str(first_case_detail.pres))
        first_case = TestCaseData(first_case, users_dict, module_dict())
        return render(request, "pages/testcase/modCase.html",
                      {"first_case": first_case,
                       "first_case_detail": first_case_detail
                       })


def del_case(request, case_id=None):
    """
    删除当前操作的测试用例
    """
    if case_id:
        case_id = case_id
    else:
        case_id = request.session[current_case_id]
    # TestCase.objects.filter(id=case_id).delete()
    return redirect("/testcase/list/")
