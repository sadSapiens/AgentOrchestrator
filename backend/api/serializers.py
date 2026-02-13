from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    file_context = serializers.CharField(required=False, allow_null=True)
    mode = serializers.CharField(default="Auto Orchestration")
    api_keys = serializers.DictField(
        child=serializers.CharField(allow_blank=True, allow_null=True),
        required=False,
        allow_null=True,
    )


class AgentInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    ver = serializers.CharField()
    status = serializers.CharField()
    role = serializers.CharField()
    color = serializers.CharField()
    cpu = serializers.IntegerField()
    mem = serializers.FloatField()
