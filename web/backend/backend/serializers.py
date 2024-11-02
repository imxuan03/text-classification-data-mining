from rest_framework import serializers
from .models import Text_Prediction


class TextPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text_Prediction
        fields = '__all__'