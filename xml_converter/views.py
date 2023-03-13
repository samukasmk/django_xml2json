from django.http import JsonResponse
from django.shortcuts import render


def upload_page(request):
    if request.method == 'POST':
        # TODO: Convert the submitted XML file into a JSON object and return to the user.
        return JsonResponse({})

    return render(request, "upload_page.html")
