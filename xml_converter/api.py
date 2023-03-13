from xml.etree.ElementTree import ParseError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from xml_converter.serializers import XMLFileSerializer
from xml_converter.logic import xml_to_dict


class ConverterViewSet(ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        serializer = XMLFileSerializer(data=request.data)
        if serializer.is_valid():
            xml_content = serializer.validated_data['file'].read()
            try:
                response_dict = xml_to_dict(xml_content)
                return Response(response_dict, status=status.HTTP_200_OK)
            except ParseError as exc:
                parser_reason = str(exc)
                response_dict = {"errors": {"parse_xml": [parser_reason]}}
                return Response(response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
