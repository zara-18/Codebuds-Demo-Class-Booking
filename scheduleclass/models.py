from django.db import models

class Contact(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    parent_email = models.EmailField()
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.phone_number} - {self.date}"
