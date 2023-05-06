from django.forms import ModelForm

from secret.models import Secret


class SecretForm(ModelForm):
    class Meta:
        model = Secret
        fields = ["secret"]
