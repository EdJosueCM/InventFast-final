# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from application.core.forms.user_form import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.utils.decorators import method_decorator

@login_required
def profile_view(request):
    return render(request, 'core/profile/profile.html', {
        'user': request.user,
        'profile': request.user.profile,
    })

@login_required
def profile_update_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('core:profile')  # redirige a la vista de perfil
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'core/profile/profile_form.html', {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Editar Perfil'
    })


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'core/user/user_list.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.select_related('profile').all()
