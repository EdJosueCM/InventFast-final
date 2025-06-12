from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from application.security.forms.auth_form import CustomUserForm
from django.contrib.auth import authenticate, login, logout


def inicio(request):
    return render(request, 'core/inicio.html')  # ✅ usar nombre de plantilla, no url name

def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con éxito. ¡Ahora puedes iniciar sesión!')
            return redirect('core:login')  # ✅ usar nombre de ruta con app_name
    else:
        form = CustomUserForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Por favor, ingresa ambos campos.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, f'Bienvenido, {user.first_name or user.username} 👋')
                return redirect('core:inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:inicio')
