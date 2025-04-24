import time
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse

from .forms import RegistrationForm
from .tokens import account_activation_token  # based on PasswordResetTokenGenerator

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create inactive user
            user = form.save(commit=False)
            user.is_active = False
            user.save()  # now in DB but inactive

            # 2. Build activation email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            mail_subject = "Activate your Summer Memory account"
            message = render_to_string(
                "registration/account_activation_email.html", {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid,
                    "token": token,
                }
            )

            # 3. Send email
            email = EmailMessage(
                mail_subject,
                message,
                'memorysummer345@gmail.com', 
                to=[form.cleaned_data["email"]],
                 headers={'X-Entity-Ref-ID': str(uuid.uuid4())}
            )
            email.send(fail_silently=False)
            time.sleep(5)

            messages.success(request,
                "Registration successful! Check your email to activate your account.")
            return redirect("journal:index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account is now activated!")
        return redirect(reverse("learning_logs:index"))
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("registration/register.html")
