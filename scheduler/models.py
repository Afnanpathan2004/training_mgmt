from django.db import models

class Training(models.Model):
    p_name = models.CharField(max_length=255)           # Program name
    name = models.CharField(max_length=255)             # Participant name
    grade = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    company= models.CharField(max_length=255, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    trainer = models.CharField(max_length=255, blank=True, null=True)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.p_name} - {self.name} ({self.date})" 