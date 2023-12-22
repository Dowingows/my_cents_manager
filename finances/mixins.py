from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UserFilteredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
