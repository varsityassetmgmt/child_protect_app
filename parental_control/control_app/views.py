from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import RestrictedURL
from .forms import RestrictedURLForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from .models import RestrictedURL
from django.http import JsonResponse
from .models import RestrictedURL
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("LOGIN SUCCESS:", user)

            return redirect('dashboard/')   # ✅ FIXED

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    # messages.success(request, "Logged out successfully ✅")
    return redirect('login')   # ✅ now works


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    user = request.user
    profile = user.userprofile   # ✅ correct

    if profile.age is not None and profile.age < 18:
        restriction = "Restricted User"
    else:
        restriction = "Full Access"

    return render(request, "dashboard.html", {
        "user": user,
        "profile": profile,
        "restriction": restriction
    })


# ---------------- CHECK URL (CORE LOGIC) ----------------


def check_url(request):
    raw_url = request.GET.get("url", "")
    domain = raw_url.replace("www.", "").lower().strip()

    # ❌ Not logged in → treat as child
    if not request.user.is_authenticated:
        blocked = RestrictedURL.objects.filter(url__icontains=domain,is_active=True).exists()

        return JsonResponse({"blocked": blocked,"reason": "Not logged in"})

    profile = request.user.userprofile

    # ❗ No age → restrict
    if profile.age is None:
        return JsonResponse({"blocked": True,"reason": "Age not set"})

    # 🔥 Check age range
    rule = RestrictedURL.objects.filter(
        url__icontains=domain,
        is_active=True,
        min_age__lte=profile.age,
        max_age__gte=profile.age
    ).first()

    if rule:
        return JsonResponse({"blocked": True,"reason": f"Blocked for age {profile.age}"})

    # ✅ Allowed
    return JsonResponse({"blocked": False,"reason": "Allowed"})




@login_required
def restricted_urls(request):
    urls = RestrictedURL.objects.all()

    return render(request, "restricted_urls.html", {
        "urls": urls
    })


 

# 🔹 LIST + SEARCH + PAGINATION
def restricted_urls(request):
    profile = request.user.userprofile

    if profile.role != "parent":
        return HttpResponseForbidden("Access denied")
    search = request.GET.get('search', '')

    urls = RestrictedURL.objects.all()

    if search:
        urls = urls.filter(url__icontains=search)

    paginator = Paginator(urls, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "restricted_urls.html", {
        "page_obj": page_obj,
        "search": search
    })


# 🔹 ADD URL
def add_url(request):
    form = RestrictedURLForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('restricted_urls')

    return render(request, "url_form.html", {"form": form})


# 🔹 UPDATE URL
def edit_url(request, id):
    obj = get_object_or_404(RestrictedURL, id=id)
    form = RestrictedURLForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('restricted_urls')

    return render(request, "url_form.html", {"form": form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')   # ✅ redirect by name











# 🔹 LIST + SEARCH + PAGINATION
def user_list(request):
    profile = request.user.userprofile

    if profile.role != "parent":
        return HttpResponseForbidden("Access denied")
    search = request.GET.get('search', '')

    users = User.objects.all()

    if search:
        users = users.filter(username__icontains=search)

    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "user_list.html", {
        "page_obj": page_obj,
        "search": search
    })


def add_user(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        return redirect('user_list')

    return render(request, "user_form.html", {"form": form})

# 🔹 EDIT USER
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    profile = user.userprofile

    user_form = UserEditForm(request.POST or None, instance=user)
    profile_form = UserProfileForm(request.POST or None, instance=profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('user_list')

    return render(request, "edit_user.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


def change_password(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        password = request.POST.get("password")
        user.set_password(password)
        user.save()
        return redirect('user_list')

    return render(request, "change_password.html", {"user": user})