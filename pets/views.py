from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from common.mixins import CheckUserIsOwner
from pets.forms import PetForm
from pets.models import Pet
from photos.models import Photo


# Create your views here.
class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'

    def get_success_url(self):
        return reverse('accounts:details', kwargs={'pk': self.object.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

# def pet_add(request: HttpRequest) -> HttpResponse:
#     form = PetForm(request.POST  or None)
#
#     if request.method == 'POST' and form.is_valid():
#         pet = form.save()
#         return redirect('accounts:details', pk=1)
#
#     context = {'form': form}
#
#     return render(request, 'pets/pet-add-page.html', context)


class PetDetailView(DetailView):
    queryset = Pet.objects.prefetch_related(
        Prefetch(
            'photo_set',
            queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
        ))
    slug_url_kwarg = 'pet_slug'
    template_name = 'pets/pet-details-page.html'


# def pet_details(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.prefetch_related(
#         Prefetch(
#             'photo_set',
#             queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
#         )
#     ).get(slug=pet_slug)
#
#     context = {'pet': pet}
#     return render(request, 'pets/pet-details-page.html', context)


class PetEditView(CheckUserIsOwner, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_success_url(self):
        return reverse('pets:details', kwargs={'username': 'username', 'pet_slug': self.object.slug})

# def pet_edit(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet) # we use instance here because its for edit
#
#     if request.method == 'POST' and form.is_valid():
#         instance = form.save()
#         return redirect('pets:details', username='username', pet_slug=instance.slug)
#
#     context = {'form': form, 'pet': pet}
#
#     return render(request, 'pets/pet-edit-page.html', context)


class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetForm

    def get_success_url(self):
        return reverse('accounts:details', kwargs={'pk': self.object.user.pk})

    def get_initial(self): # for filled fields to the form
        return self.object.__dict__

# def pet_delete(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)  # we use instance here because its for edit
#
#     if request.method == 'POST' and form.is_valid():
#         pet.delete()
#         return redirect('accounts:details', pk=1)
#
#     context = {'form': form, 'pet': pet}
#
#     return render(request, 'pets/pet-delete-page.html', context)
