from django.urls import path
from .views import ListCreateAPIView, SensorView, MeasurementView, SensorUpdate

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('demo/', ListCreateAPIView.as_view()),
    path('demo/<pk>/', SensorView.as_view()),
    path('measurement/', MeasurementView.as_view()),
    path('sensor_edit/<pk>/', SensorUpdate.as_view()),

]
