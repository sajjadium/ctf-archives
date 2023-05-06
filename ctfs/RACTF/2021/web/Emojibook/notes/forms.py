import json
import re

from django import forms
from django.forms import Textarea

from notes.models import Note


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["name", "body"]
        widgets = {
            "body": Textarea(attrs={"cols": 60, "rows": 20}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NoteCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NoteCreateForm, self).save(commit=False)
        instance.author = self.user
        instance.body = instance.body.replace("{{", "").replace("}}", "").replace("..", "")

        with open("emoji.json") as emoji_file:
            emojis = json.load(emoji_file)

            for emoji in re.findall("(:[a-z_]*?:)", instance.body):
                instance.body = instance.body.replace(emoji, "{{" + emojis[emoji.replace(":", "")] + ".png}}")

        if commit:
            instance.save()
            self._save_m2m()

        return instance

