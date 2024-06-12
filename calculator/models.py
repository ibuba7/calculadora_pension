from django.db import models

class InfoFin_Cat(models.Model):
    variable = models.CharField(max_length=100)
    value = models.FloatField()


class Comisiones_Cat(models.Model):
    afore = models.CharField(max_length=100)
    value = models.FloatField()

class RentasVitalicias_Cat(models.Model):
    edad = models.IntegerField()
    Ax_h = models.FloatField()
    Ax_m = models.FloatField()

class CuotaSocial_Cat(models.Model):
    rango_min = models.FloatField()
    rango_max = models.FloatField()
    valor = models.FloatField()

    def __str__(self):
        return f"{self.rango_min} - {self.rango_max}: {self.valor}"

class PG_Cat(models.Model):
    rango_min = models.FloatField()
    rango_max = models.FloatField()
    edad = models.FloatField()
    sem1 = models.FloatField()
    sem2 = models.FloatField()
    sem3 = models.FloatField()
    sem4 = models.FloatField()
    sem5 = models.FloatField()
    sem6 = models.FloatField()
    sem7 = models.FloatField()
    sem8 = models.FloatField()
    sem9 = models.FloatField()
    sem10 = models.FloatField()
    sem11 = models.FloatField()

    def __str__(self):
        return f"Rango: {self.rango_min}-{self.rango_max}"
    
class SemMin_Cat(models.Model):
    y_2021 = models.IntegerField()
    y_2022 = models.IntegerField()
    y_2023 = models.IntegerField()
    y_2024 = models.IntegerField()
    y_2025 = models.IntegerField()
    y_2026 = models.IntegerField()
    y_2027 = models.IntegerField()
    y_2028 = models.IntegerField()
    y_2029 = models.IntegerField()
    y_2030 = models.IntegerField()
    y_2031 = models.IntegerField()

class ContrPatr_Cat(models.Model):
    rango_min = models.FloatField()
    rango_max = models.FloatField()
    y_2023 = models.FloatField()
    y_2024 = models.FloatField()
    y_2025 = models.FloatField()
    y_2026 = models.FloatField()
    y_2027 = models.FloatField()
    y_2028 = models.FloatField()
    y_2029 = models.FloatField()
    y_2030 = models.FloatField()

    def __str__(self):
        return f"Rango: {self.rango_min}-{self.rango_max}"