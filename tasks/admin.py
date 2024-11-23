from django.core.mail import send_mail
from django.contrib import admin, messages
from .models import Task
from django.urls import path, reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User  # Replace with your custom User model if applicable
from django.utils.http import urlencode
from django.utils.html import format_html

@admin.action(description="Invite selected users via email")
def invite_user(modeladmin, request, queryset):
    for user in queryset:
        if user.email:
            # Generate a registration URL with a query parameter for the user
            base_url = request.build_absolute_uri(reverse("register"))  # Update "register" with your registration view's name
            query_string = urlencode({"email": user.email})
            registration_link = f"{base_url}?{query_string}"

            # Send the invitation email
            send_mail(
                subject="You're Invited to Join Our Platform",
                message=f"Hi {user.username},\n\nYou're invited to join our platform. Click the link below to register:\n\n{registration_link}\n\nThank you!",
                from_email="admin@yourdomain.com",  # Replace with your email
                recipient_list=[user.email],
                fail_silently=False,
            )
        else:
            modeladmin.message_user(request, f"User {user.username} has no email address.", level="warning")

# Customize UserAdmin to include the invite action
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_staff"]
    actions = [invite_user]

# Register User model with CustomUserAdmin
admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin)  # Register with the new admin

# Customize the Task admin panel
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    actions = [invite_user]
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('invite/', self.admin_site.admin_view(invite_user), name='task-invite-user'),
        ]
        return custom_urls + urls

admin.site.register(Task, TaskAdmin)

# Do not register SocialApp again
# If you need to customize SocialAppAdmin, subclass it and unregister/re-register it
