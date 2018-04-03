{%- if cookiecutter.drf == 'yes' %}
from django.conf.urls import url
from rest_framework.routers import DefaultRouter


from accounts.views import ValidateUniqueFields, MyAccount, Users, CreateAccount, ChangePassword

app_name = 'accounts'

router = DefaultRouter()
router.register(r'', Users, base_name='users')

urlpatterns = [
    url(r'validate', ValidateUniqueFields.as_view()),
    url(r'change-password', ChangePassword.as_view()),
    url(r'me', MyAccount.as_view()),
    url(r'create', CreateAccount.as_view()),
]

urlpatterns += router.urls
{%- endif %}
{%- if cookiecutter.drf != 'yes' %}
urlpatterns = []
{% endif %}
