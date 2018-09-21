from django.shortcuts import render

from script.form import ScriptUploadForm
from script.models import ScriptType
from testcase.models import CaseModule, TestCase
import os
import time
import utils.utilsFunc


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


def _create_script_folder(script_type: list):
    """用于在storage中的脚本分类文件夹"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_dir = os.path.join(BASE_DIR, "storage/scripts")
    dirs_need_created = [folder for folder in script_type if folder not in storage_dir]
    if len(dirs_need_created) == 0:
        return
    for folder_name in dirs_need_created:
        os.mkdir(os.path.join(storage_dir, folder_name))


def _create_script_file(file, s_type):
    """在指定的目录下创建文件
        为了解决重名问题，所有的文件在传输到服务器后，名称将统一变为name+当前毫秒数+后缀名的方式
    """
    index_of_suffix = str(file.name).rindex(".")
    file_name = file.name[0:index_of_suffix] + "." + str(time.time()) + file.name[
                                                                        index_of_suffix:]
    new_file_path = os.path.join(utils.utilsFunc.path_script_storage(), s_type)
    try:
        new_file = open(os.path.join(new_file_path, file_name), "w", encoding="utf-8")
        with open(file, "w", encoding="utf-8", errors="strict") as origin_file:
            for line in origin_file.read():
                new_file.write(line)
    except ValueError:
        return False
    else:
        return True
