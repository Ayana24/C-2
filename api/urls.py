from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerevalAddedViewSet
from .views import SubmitDataView

router = DefaultRouter()
router.register(r'perevals', PerevalAddedViewSet, basename='pereval')

urlpatterns = [
    path('', include(router.urls)),
    path('submitData/', SubmitDataView.as_view(), name='submit-data-list'),
    path('submitData/<int:id>/', SubmitDataView.as_view(), name='submit-data-detail'),
]