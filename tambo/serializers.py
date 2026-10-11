from rest_framework import serializers
from .models import PushSubscription
from rest_framework import serializers
from .models import Vaca

class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = '__all__'


class VacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaca
        fields = '__all__'