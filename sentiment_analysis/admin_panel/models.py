from django.db import models

class Consultation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    reference_no = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consultation.reference_no} - {self.sentiment}"