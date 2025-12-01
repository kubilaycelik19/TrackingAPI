from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.category_name}"

class Expense(models.Model):
    expense_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2 ,verbose_name="Fiyat")
    description = models.CharField(max_length=100, verbose_name="Açıklama")
    date = models.DateField()

    def __str__(self):
        return f"{self.category.name} - {self.amount} TL"
    
# shell modunda category ekleme => Category.objects.create(category_name="Kategori Adı")
# shell modunda expense ekleme => Expense.objects.create(expense_category_id=1, amount=100.50, description="Açıklama", date="2024-06-01")
# shell modunda expense listeleme => Expense.objects.all()
