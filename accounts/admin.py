from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from accounts.models import (UserBasicDetails)
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    form = UserChangeForm

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('date_joined',)}),  # Removed 'last_login'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def change_password(self, request, id, form_url=''):
        if request.method == 'POST':
            user = self.get_object(request, id)
            form = self.form(user, request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password1']
                if user.check_password(new_password):
                    messages.error(request, "You have already used this password. Please choose a different one.")
                    return self.response_change(request, user)
                user.set_password(new_password)
                user.save()
                return self.response_change(request, user)
        else:
            form = self.form(user)
        return self.render_change_form(request, context={'form': form, 'change': True, 'is_popup': "_popup" in request.POST, 'save_as': False, 'has_delete_permission': False, 'has_change_permission': True, 'has_absolute_url': False, 'opts': self.model._meta, 'original': user}, form_url=form_url, add=True)

@admin.register(UserBasicDetails)
class UserBasicDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'image_tag', 'user__phone_number', 'date_of_birth', 'aadhaar_number')
    list_display_links = ('user',)
    search_fields = ('user__phone_number', 'user__email', 'user__first_name', 'user__last_name', 'date_of_birth', 'aadhaar_number', 'MPIN')

    def get_ordering(self, request):
        return ['user__email']