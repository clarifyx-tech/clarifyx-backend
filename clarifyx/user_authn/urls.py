from django.urls import include, path

from clarifyx.user_authn.api.v1 import urls as v1_user_authn_api_urls

urlpatterns = [
    path("v1/", include((v1_user_authn_api_urls, "v1"), namespace="v1")),
]
