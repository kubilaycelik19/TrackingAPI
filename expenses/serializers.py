from rest_framework import serializers
from rest_framework import request
from rest_framework import validators
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(read_only=True) alternatif

    class Meta:
        model = Expense
        fields = '__all__'

        read_only_fields = ['user']  # 'user' alanı sadece okunabilir olacak

    def validate_amount(self, value):
        """
        'Amount' icin ozel kontrol.
        """
        if value <= 0 :
            raise serializers.ValidationError("Hatali deger!")
        else: return value

class ReceiptAnalysisSerializer(serializers.Serializer):
    image_url = serializers.CharField(required=True, help_text="Analiz edilecek fişin URL'i veya dosya yolu")



