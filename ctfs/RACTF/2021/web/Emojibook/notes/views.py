import base64
import os
import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from notes.forms import NoteCreateForm
from notes.models import Note


class RegisterFormView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    model = User
    success_url = "/"


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user)
        return render(request, "index.html", {"user": request.user, "notes": notes})
    return render(request, "index.html", {"user": request.user})


def create_note(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NoteCreateForm(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(redirect_to=reverse("note", kwargs={"pk": instance.pk}))
    else:
        form = NoteCreateForm(user=request.user)
    return render(request, "create.html", {"form": form})


def view_note(request: HttpRequest, pk: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=pk)
    text = note.body
    for include in re.findall("({{.*?}})", text):
        print(include)
        file_name = os.path.join("emoji", re.sub("[{}]", "", include))
        with open(file_name, "rb") as file:
            text = text.replace(include, f"<img src=\"data:image/png;base64,{base64.b64encode(file.read()).decode('latin1')}\" width=\"25\" height=\"25\" />")

    return render(request, "note.html", {"note": note, "text": text})
