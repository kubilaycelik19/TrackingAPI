from rest_framework import serializers
from rest_framework import request
from rest_framework import validators
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'

    def validate_amount(self, value):
        """
        'Amount' icin ozel kontrol.
        """
        if value <= 0 :
            raise serializers.ValidationError("Hatali deger!")
        else: return value



