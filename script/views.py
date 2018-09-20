from django.shortcuts import render


# Create your views here.


def init_upload_page(request):
    return render(request, "pages/script/upload.html")
