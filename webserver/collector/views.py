from django.shortcuts import render, HttpResponse
from .models import Collector
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseServerError
from .utils import collectors_filter, process_upload
from django.core.paginator import Paginator
from django.urls import reverse

@csrf_exempt
def accounts(request):
    if request.method == 'GET':
        min_balance = request.GET.get('min_balance', None)
        if min_balance:
            try:
                min_balance = float(min_balance)
            except ValueError:
                return JsonResponse({"error": "min_balance must be a number."}, status=400)
        max_balance = request.GET.get('max_balance', None)
        if max_balance:
            try:
                max_balance = float(max_balance)
            except ValueError:
                return JsonResponse({"error": "max_balance must be a number."}, status=400)
        consumer_name = request.GET.get('consumer_name', None)
        status = request.GET.get('status', None)
        if status:
            if status == 'collected':
              status = 'PAID_IN_FULL'
            status = status.upper()
            valid_status = ['PAID_IN_FULL', 'IN_COLLECTION', 'INACTIVE']
            if status not in valid_status:
                return JsonResponse({"error": "status is not valid."}, status=400)
        
        collectors = collectors_filter(
            min_balance=min_balance,
            max_balance=max_balance,
            consumer_name=consumer_name,
            status=status
        )
        
        paginator = Paginator(collectors, 30)  
        page = paginator.get_page(request.GET.get('page'))

        url = request.build_absolute_uri(reverse('accounts')) + '?page=' 
        next_page, prev_page = None, None
        if page.has_next():
          next_page = url + str(page.next_page_number())
        if page.has_previous():
          prev_page = url + str(page.previous_page_number())


        return JsonResponse({
            'data': page.object_list,
            'next_page': next_page,
            'prev_page': prev_page,
        })
    else:
        return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def consumers(request):
    if request.method == 'GET':
        consumer_names = Collector.objects.values_list('consumer_name', flat=True).distinct()

        paginator = Paginator(consumer_names, 50) 
        page = paginator.get_page(request.GET.get('page'))

        url = request.build_absolute_uri(reverse('consumers')) + '?page=' 
        next_page, prev_page = None, None
        if page.has_next():
          next_page = url + str(page.next_page_number())
        if page.has_previous():
          prev_page = url + str(page.previous_page_number())

        return JsonResponse({
            'data': list(page),
            'next_page': next_page,
            'prev_page': prev_page,
        })

    else:
        return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                process_upload(file)
                return HttpResponse("Upload success.", status=200)
            except Exception as e:
                return HttpResponseServerError(str(e), status=500)
        else:
            return HttpResponse("File not found.", status=400)
    else:
        return HttpResponse("Invalid request.", status=400)
