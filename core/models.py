from django.db import models
from django.urls import reverse

class VirtualMachine(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    cpu = models.IntegerField(null=False, verbose_name='Количество ядер центрального процессора')
    ram = models.IntegerField(null=False, verbose_name='Оперативная память')
    sata = 'sata'
    ssd = 'ssd'
    sas = 'sas'
    hdd_type_choices = [
        (sata, 'sata'),
        (ssd, 'ssd'),
        (sas, 'sas'),
    ]
    hdd_type = models.CharField(max_length=15, choices=hdd_type_choices, verbose_name='Тип жёсткого диска')
    hdd_capacity = models.IntegerField(null=False, verbose_name='Объём памяти жёсткого диска')

    def __str__(self):
        return 'cpu - %s, ram - %s, hdd_type - %s, hdd_capacity - %s' % (self.cpu ,self.ram ,self.hdd_type ,self.hdd_capacity)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    class Meta:
        verbose_name='Виртуальную машину'
        verbose_name_plural='Виртуальные машины'
