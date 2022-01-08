from django.views.decorators.csrf import csrf_exempt

#404 page_not_found error
@csrf_exempt
def page_not_found(request):
    return render(request,'page_not_found.html',RequestContext(request))

#500 server_error
@csrf_exempt
def server_error(request):
    return render(request,"server_error.html")

