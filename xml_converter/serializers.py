from rest_framework.serializers import Serializer, FileField


class XMLFileSerializer(Serializer):
    file = FileField()

    class Meta:
        fields = ['file']
