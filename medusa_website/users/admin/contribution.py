from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import QuerySet

from medusa_website.users.models import Contribution


@admin.action(description="Sign off selected contributions")
def sign_off_contributions(modeladmin, request, queryset: QuerySet[Contribution]):
    assert request.user.has_contrib_sign_off_permission()
    for contrib in queryset:
        contrib.sign(signer=request.user)


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "type", "requires_signing", "signed_off_date", "signed_off_by"]
    list_display_links = ["type"]
    search_fields = ["user", "type"]
    list_filter = ["requires_signing", "type", "is_signed_off", "signed_off_date"]
    readonly_fields = ["requires_signing", "is_signed_off", "signed_off_date"]
    actions = [sign_off_contributions]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["signed_off_by"].queryset = Group.objects.get(name="Contributions Sign Off").user_set.all()
        return form
