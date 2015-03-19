from django.db import models

class Ticket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    progress = models.IntegerField(default=0)
    # priority = models.IntegerField(choices=(1,2,3,4,5), default=1)
    # hardness = models.IntegerField(choices=(1,2,3,4,5), default=1)
    priority = models.IntegerField(default=1)
    hardness = models.IntegerField(default=1)
    owner = models.ForeignKey('auth.User', related_name='tickets')

    class Meta:
        ordering = ('created',)
