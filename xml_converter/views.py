from xml.etree.ElementTree import ParseError
from django.http import JsonResponse
from django.shortcuts import render
from xml_converter.forms import XMLFileForm
from xml_converter.logic import xml_to_dict


def upload_page(request):
    # render frontend page
    if request.method == 'GET':
        form = XMLFileForm()

    # return json content
    elif request.method == 'POST':
        form = XMLFileForm(request.POST, request.FILES)
        # invalid form fields
        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=400)

        try:
            # parsing xml content
            xml_content = form.cleaned_data['file'].read()
            response_dict = xml_to_dict(xml_content)
            return JsonResponse(response_dict, status=200)
        except ParseError as exc:
            # failed on parsing file
            parser_reason = str(exc)
            response_dict = {"errors": {"parse_xml": [parser_reason]}}
            return JsonResponse(response_dict, status=422)

    return render(request, 'upload_page.html', {'form': form})
