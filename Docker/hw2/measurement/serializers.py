from rest_framework import serializers

# TODO: опишите необходимые сериализаторы
from rest_framework import serializers
from .models import Sensor
from .models import Measurement

class SensorSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Sensor.objects.create(**validated_data)
    class Meta:
        model = Sensor
        fields = ['id','name', 'description']

class MeasurementSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     return Measurement.objects.create(**validated_data)
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'sensor']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']


# class SensorSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     description = serializers.CharField()