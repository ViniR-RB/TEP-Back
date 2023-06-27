from rest_framework import serializers

from api.models import *
from user.models import CustomUser, Investor


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'

class TransactionFromStock(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields= '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    operation = serializers.ChoiceField(choices=['C', 'V'], default='C', write_only=True)
    type_operation = serializers.SerializerMethodField()
    total_operation = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    price_medium = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = CustomUser.objects.get(id=self.context['request'].user.id)
        print(user)
        self.fields['investor'] = serializers.HiddenField(default=user)

    def create(self,validated_data):
        object_data = Transaction.objects.create(**validated_data)
        return object_data

    def get_type_operation(self, obj):
        return obj.get_operation_display()

    def get_total_price(self, obj):
        return obj.calculate_price_total()

    def get_total_operation(self,obj):
        return obj.calculate_total_value()
    def get_price_medium(self,obj):
        return obj.calculate_price_medium()



