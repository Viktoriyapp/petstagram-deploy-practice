from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView

from common.mixins import CheckUserIsOwner
from photos.forms import PhotoForm
from photos.models import Photo


# Create your views here.

def photo_add(request: HttpRequest) -> HttpResponse:
    form = PhotoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        return redirect('common:home')

    context = {'form': form}

    return render(request, 'photos/photo-add-page.html', context)

def photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.prefetch_related('tagged_pets', 'like_set', 'comment_set').get(pk=pk)

    context = {'photo': photo}

    return render(request, 'photos/photo-details-page.html', context)


class PhotoEditView(LoginRequiredMixin, CheckUserIsOwner, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self):
        return reverse('photos:details', kwargs={'pk': self.object.pk})


# def photo_edit(request: HttpRequest, pk: int) -> HttpResponse:
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)
#
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('photos:details', photo.pk)
#
#     context = {'form': form}
#
#     return render(request, 'photos/photo-edit-page.html', context)


class PhotoDeleteView(LoginRequiredMixin, CheckUserIsOwner, DeleteView):
    model = Photo
    success_url = reverse_lazy('common:home')


# def photo_delete(request: HttpRequest, pk: int) -> HttpResponse:
#     photo = Photo.objects.get(pk=pk).delete()
#     return redirect('common:home')