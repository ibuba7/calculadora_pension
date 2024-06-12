from django.shortcuts import render
from django.http import HttpResponse
from . import plot_generator
import csv

def home(request):
    return render(request, 'calculator/home.html')


def result(request):
    if request.method == 'POST':
            form_data = {
                'fecha_nacimiento': request.POST['fecha_nacimiento'],
                'salario_base': request.POST['salario_base'],
                'imss_1997': request.POST['imss_1997'],
                'cuota_social': request.POST['cuota_social'],
                'saldo_aportaciones_voluntarias': request.POST['saldo_aportaciones_voluntarias'],
                'infonavit_1997': request.POST['infonavit_1997'],
                'aportaciones_voluntarias_mensuales': request.POST['aportaciones_voluntarias_mensuales'],
                'sexo': request.POST['sexo'],
                'semanas_cotizadas': request.POST['semanas_cotizadas'],
                'cesantia_vejez': request.POST['cesantia_vejez'],
                'formalidad': request.POST['formalidad'],
                'afore': request.POST['afore'],
            }
            
            # Pass the form_data to the plot_generator
            plot_generator.generate_plot(form_data)

            extra_data = plot_generator.generate_plot(form_data)

    data = []
    show_red_legend = False
    show_yellow_legend = False
    with open('data_pensiones.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Negativa de Pensión'] == '1':
                show_red_legend = True
            if row['Pensión Garantizada'] == '1':
                show_yellow_legend = True
            data.append({
                'Edad': row['Edad de Retiro'],
                'Pensión': row['Pensión'],
                'Tasa_de_Reemplazo': row['Tasa de Reemplazo'],
                'Pensión_con_AV': row['Pensión con AV'],
                'Tasa_de_Reemplazo_con_AV': row['Tasa de Reemplazo con AV'],
                'Negativa_de_Pensión': row['Negativa de Pensión'],
                'Pensión_Garantizada': row['Pensión Garantizada']
            })

    return render(request, 'calculator/result.html', {'data': data, 'show_red_legend': show_red_legend, 'show_yellow_legend': show_yellow_legend, 'extra_data': extra_data})