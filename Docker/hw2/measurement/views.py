# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


# @api_view(['GET', 'POST'])
# def ListCreateAPIView(request):
#     if request.method == 'GET':
#         sensors = Sensor.objects.all()
#         ser = SensorSerializer(sensors, many=True)
#         return Response(ser.data)
#
#     if request.method == 'POST':
#         return Response({'status': 'ok'})

class ListCreateAPIView(APIView):
    def get(self, request):
        sensors = Sensor.objects.all()
        ser = SensorDetailSerializer(sensors, many=True)
        return Response(ser.data)

    def post(self, request):
        sensor = request.data.get('sensor')
        serializer = SensorSerializer(data=sensor)
        if serializer.is_valid(raise_exception=True):
            sensor_saved = serializer.save()
        return Response({"success": "Sensor '{}' created successfully".format(sensor_saved.name)})

    # def put(self, request, pk):
    #     saved_article = get_object_or_404(Article.objects.all(), pk=pk)
    #     data = request.data.get('articles')
    #     serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         article_saved = serializer.save()
    #     return Response({
    #         "success": "Article '{}' updated successfully".format(article_saved.title)
    #     })

class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class SensorUpdate(UpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class MeasurementView(APIView):
    def post(self, request):
        measurement = request.data.get('measurement')
        print(measurement)
        serializer = MeasurementSerializer(data=measurement)
        if serializer.is_valid(raise_exception=True):
            measurement_saved = serializer.save()
        return Response({"success": "Measurement '{}' created successfully".format(measurement_saved.sensor)})



