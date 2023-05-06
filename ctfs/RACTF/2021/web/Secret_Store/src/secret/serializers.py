from rest_framework import serializers

from secret.models import Secret


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ["id", "value", "owner", "last_updated", "created"]
        read_only_fields = ["owner", "last_updated", "created"]
        extra_kwargs = {"value": {"write_only": True}}

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        if Secret.objects.filter(owner=self.context["request"].user):
            return super(SecretSerializer, self).update(Secret.objects.get(owner=self.context['request'].user), validated_data)
        return super(SecretSerializer, self).create(validated_data)
