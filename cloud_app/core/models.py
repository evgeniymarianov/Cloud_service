from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.IntegerField(null=False, default=1000)
    country = models.CharField(max_length=30, null=False, default='Russia')


class Network(models.Model):
    name = models.CharField(max_length=30)


class VirtualMachine(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    cpu = models.IntegerField(null=False, verbose_name='Количество ядер центрального процессора')
    ram = models.IntegerField(null=False, verbose_name='Оперативная память')
    hdd_type = models.CharField(choices = (
            ('sata', 'sata'),
            ('ssd', 'ssd'),
            ('sas', 'sas'),
        ),
        max_length=15, verbose_name='Тип жёсткого диска'
    )
    hdd_capacity = models.IntegerField(null=False, verbose_name='Объём памяти жёсткого диска')
    current_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    networks = models.ManyToManyField(Network)
    cost = models.IntegerField(null=False, default=0)

    def __str__(self):
        return 'cpu - %s, ram - %s, hdd_type - %s, hdd_capacity - %s' % (self.cpu ,self.ram ,self.hdd_type ,self.hdd_capacity)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    class Meta:
        verbose_name='Виртуальную машину'
        verbose_name_plural='Виртуальные машины'


class AdditionalHdd(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    hdd_type = models.CharField(choices = (
            ('sata', 'sata'),
            ('ssd', 'ssd'),
            ('sas', 'sas'),
        ),
        max_length=15, verbose_name='Тип жёсткого диска'
    )
    hdd_capacity = models.IntegerField(null=False, verbose_name='Объём памяти жёсткого диска')
    virtual_machine = models.ForeignKey(VirtualMachine, on_delete=models.CASCADE)
    cost = models.IntegerField(null=False, default=0)


class Report(models.Model):
    """docstring forReport."""
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=300, null=False, default='Russia')
