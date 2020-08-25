from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import MyTokenObtainPairView
import reviews


urlpatterns = [
    path("admin/", admin.site.urls),
    path("redoc/", TemplateView.as_view(template_name="redoc.html"), name="redoc"),
]

urlpatterns += [
    path(
        "api/v1/",
        include(
            [
                path(
                    "token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"
                ),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
                ),
                path("", include("users.urls")),
                path("", include("contents.urls")),
                re_path("titles/(?P<title_id>\d+)/reviews/", include("reviews.urls")),
                path("api-auth/", include("rest_framework.urls")),
            ]
        ),
    )
]
