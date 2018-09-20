from django.shortcuts import render

from script.form import ScriptUploadForm
from script.models import ScriptType
from testcase.models import CaseModule, TestCase


# Create your views here.


def init_upload_page(request):
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
        # 获取脚本的分类列表
        script_types = [s_type.name for s_type in ScriptType.objects.all()]
        # 请求用例列表
        case_queryset = TestCase.objects.all()
        # 根据用例列表来进行分组，生成DICT
        module_case_dict = {}
        for _id in module_dict.keys():
            case_list = [case for case in case_queryset if case.case_module == _id]
            module_case_dict[module_dict.get(_id).name] = case_list
        # 传输数据说明：
        # module_case_list：NAME:LIST
        # user_dict：用户ID:NAME 字典
        # first_case：第一个需要显示的case
        # 将当前操作的测试用例ID写入到session
        return render(request, "pages/script/upload.html",
                      {"module_case_dict": module_case_dict, "types": script_types})
    if request.method == "POST":
        """请求方式为POST，即为提交脚本数据"""
        upload_form = ScriptUploadForm(request.POST)
        if upload_form.is_valid():
            script_file = upload_form.scriptFile
            script_case = upload_form.case
            script_type = upload_form.scriptType
            script = ScriptType
