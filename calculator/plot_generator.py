from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter
from calculator.models import InfoFin_Cat
from calculator.models import CuotaSocial_Cat
from calculator.models import PG_Cat
from calculator.models import SemMin_Cat
from calculator.models import Comisiones_Cat
from calculator.models import RentasVitalicias_Cat
from calculator.models import ContrPatr_Cat
from datetime import datetime
import csv

def get_value_for_cuota_social(input_value):
    try:
        range_value = CuotaSocial_Cat.objects.get(rango_min__lte=input_value, rango_max__gte=input_value)
        return range_value.valor
    except CuotaSocial_Cat.DoesNotExist:
        return 0
    
def get_value_for_comisiones(input_value):
    try:
        range_value = Comisiones_Cat.objects.get(afore=input_value)
        return range_value.value
    except Comisiones_Cat.DoesNotExist:
        return 'NA'
    
def get_values_for_PG(input_value, age):
    # Filter the rows that match the input_value in the range and the specific age
    matching_rows = PG_Cat.objects.filter(
        Q(rango_min__lte=input_value) & Q(rango_max__gte=input_value) & Q(edad=age)
    )

    if not matching_rows.exists():
        return None

    # Retrieve the first matching row
    matching_row = matching_rows.first()

    # Construct the list of values to return
    row_values = [
        matching_row.rango_min,
        matching_row.rango_max,
        matching_row.edad,
        matching_row.sem1,
        matching_row.sem2,
        matching_row.sem3,
        matching_row.sem4,
        matching_row.sem5,
        matching_row.sem6,
        matching_row.sem7,
        matching_row.sem8,
        matching_row.sem9,
        matching_row.sem10,
        matching_row.sem11
    ]

    return row_values

def get_sem_min(year):
    # Construct the column name based on the given year
    column_name = f'y_{year}'
    
    # Ensure the column name is valid
    if not hasattr(SemMin_Cat, column_name):
        raise ValueError(f"Invalid year: {year}. Column '{column_name}' does not exist.")
    
    # Retrieve all values from the specified column
    values = SemMin_Cat.objects.values_list(column_name, flat=True)
    
    # Convert QuerySet to a list
    values_list = list(values)
    
    return values_list

def get_value_by_range_and_year(value, year):
    try:
        # Filter the objects where the value is between rango_min and rango_max
        contr_patr_obj = ContrPatr_Cat.objects.get(rango_min__lte=value, rango_max__gte=value)
        
        # Retrieve the corresponding value based on the specified year
        year_column = f'y_{year}'
        
        # Check if the year column exists in the model
        if not hasattr(contr_patr_obj, year_column):
            raise ValueError(f"Invalid year: {year}. No such column y_{year} in ContrPatr_Cat model.")
        
        return getattr(contr_patr_obj, year_column)
    
    except ObjectDoesNotExist:
        raise ValueError(f"No data found for value {value} within any range.")
    except Exception as e:
        raise ValueError(str(e))

def find_closest_value(sem, pg, value):
    # Initialize variables to store the closest index and closest value
    closest_index = -1

    # Iterate through the sem list
    for i in range(len(sem)):
        # Check if the current value in sem is less than or equal to the given value
        if sem[i] <= value:
            # Update the closest value and index
            closest_index = i
        else:
            # If we find a value greater than the given value, break the loop
            break

    # If no suitable value was found, return None or raise an exception
    if closest_index == -1:
        raise ValueError("No valid value found in the list that is less than or equal to the given value")

    # Retrieve the corresponding value from pg
    corresponding_pg_value = pg[closest_index]

    return corresponding_pg_value

def get_ax_value(age, gender):
    try:
        # Retrieve the row corresponding to the given age (edad)
        rentas_vitalicias_row = RentasVitalicias_Cat.objects.get(edad=age)
        
        # Check the gender and retrieve the corresponding value
        if gender == 'M':
            return rentas_vitalicias_row.Ax_h
        elif gender == 'F':
            return rentas_vitalicias_row.Ax_m
        else:
            raise ValueError("Invalid gender. Please use 'M' for male or 'F' for female.")
    
    except ObjectDoesNotExist:
        raise ValueError(f"No data found for age {age}.")
    
def currency(x, pos):
    'The two args are the value and tick position'
    return '${:,.0f}'.format(x)

def generate_plot(data):
    fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d')
    salario_base = float(data['salario_base'].replace('$', '').replace(',', ''))
    imss_1997 = float(data['imss_1997'].replace('$', '').replace(',', ''))
    cuota_social = float(data['cuota_social'].replace('$', '').replace(',', ''))
    saldo_aportaciones_voluntarias = float(data['saldo_aportaciones_voluntarias'].replace('$', '').replace(',', ''))
    infonavit_1997 = float(data['infonavit_1997'].replace('$', '').replace(',', ''))
    aportaciones_voluntarias_mensuales = float(data['aportaciones_voluntarias_mensuales'].replace('$', '').replace(',', ''))
    sexo = data['sexo']
    semanas_cotizadas = int(data['semanas_cotizadas'].replace(',', ''))
    cesantia_vejez = float(data['cesantia_vejez'].replace('$', '').replace(',', ''))
    formalidad = float(data['formalidad'].strip('%'))/100
    afore = data['afore']
    comision = get_value_for_comisiones(afore) / 100
    tasa_rend = InfoFin_Cat.objects.get(variable='tasa_rend').value
    tasa_viv = InfoFin_Cat.objects.get(variable='tasa_viv').value
    UMA = InfoFin_Cat.objects.get(variable='UMA').value
    SM = InfoFin_Cat.objects.get(variable='salario_min').value
    porc_contr_tr = InfoFin_Cat.objects.get(variable='porc_contr_tr').value
    porc_contr_ret = InfoFin_Cat.objects.get(variable='porc_contr_ret').value
    porc_contr_viv = InfoFin_Cat.objects.get(variable='porc_contr_viv').value

    today_date = datetime.now()
    today_year = today_date.year
    edad = today_date.year - fecha_nacimiento.year - ((today_date.month, today_date.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    if edad >= 65:
        edades = [edad]
    else:
        edades = list(range(edad, 66))
    years = list(range(today_year, today_year + len(edades)))
    if salario_base > 25 * UMA:
        salario_cot = 25 * UMA
    elif salario_base < SM:
        salario_cot = SM
    else:
        salario_cot = salario_base

    salario_uma = salario_cot/UMA
    
    porc_contr = []
    for i in years:
        sal_uma = salario_uma
        an = i
        if salario_cot < SM: sal_uma = 1
        if i > 2030: an = 2030
        porc_contr.append(get_value_by_range_and_year(sal_uma, an) + porc_contr_tr)

    contr_CV = [x * salario_cot * formalidad * 12 for x in porc_contr]
    CS = get_value_for_cuota_social(sal_uma) * 365 * formalidad

    saldo_CV_CS = [cesantia_vejez + cuota_social]
    contr_CV_CS = [cesantia_vejez + cuota_social]
    for i in range(0,len(years) - 1):
        saldo_CV_CS.append(saldo_CV_CS[i] * (1 + tasa_rend - comision) + (contr_CV[i] + CS) * (1 + (tasa_rend - comision)/2))
        contr_CV_CS.append(contr_CV_CS[i] + contr_CV[i] + CS)
        
    rend_CV_CS = [x - y for x,y in zip(saldo_CV_CS, contr_CV_CS)]

    contr_ret =  porc_contr_ret * salario_cot * formalidad * 12
    saldo_ret = [imss_1997]
    contr_ret_l = [imss_1997]
    for i in range(0,len(years) - 1):
        saldo_ret.append(saldo_ret[i] * (1 + tasa_rend - comision) + contr_ret * (1 + (tasa_rend - comision)/2))
        contr_ret_l.append(contr_ret_l[i] + contr_ret)
        
    rend_ret = [x - y for x,y in zip(saldo_ret, contr_ret_l)]
    saldo_total = [x + y for x,y in zip(saldo_CV_CS, saldo_ret)]

    contr_av =  aportaciones_voluntarias_mensuales * formalidad * 12
    saldo_av = [saldo_aportaciones_voluntarias]
    contr_av_l = [saldo_aportaciones_voluntarias]
    for i in range(0,len(years) - 1):
        saldo_av.append(saldo_av[i] * (1 + tasa_rend - comision) + contr_av * (1 + (tasa_rend - comision)/2))
        contr_av_l.append(contr_av_l[i] + contr_av)
        
    rend_av = [x - y for x,y in zip(saldo_av, contr_av_l)]
    saldo_total_av = [x + y for x,y in zip(saldo_total, saldo_av)]

    contr_viv =  porc_contr_viv * salario_cot * formalidad * 12
    saldo_viv = [infonavit_1997]
    for i in range(0,len(years) - 1):
        saldo_viv.append(saldo_viv[i] * (1 + tasa_viv) + contr_viv * (1 + (tasa_viv)/2))

    semanas_proy = [semanas_cotizadas]
    for i in range(0, len(years) - 1):
        semanas_proy.append(round(semanas_proy[i] + 52 * formalidad,0))

    semanas_req = []
    RV = []
    pg = []
    pension = []
    pension_av = []
    dict_pg = []
    dict_neg = []
    ret_list = [index for index, edades in enumerate(edades) if edades >= 60]
    for i in ret_list:
        an = years[i]
        if an > 2031: an = 2031
        sem_min = get_sem_min(an)
        semanas_req.append(sem_min[0])
        RV_value = get_ax_value(edades[i], sexo)
        if edad > 65:
            pg_l = get_values_for_PG(sal_uma, 65)[3:]
        else:
            pg_l = get_values_for_PG(sal_uma, edades[i])[3:]
        sems = semanas_proy[i]
        if sems < sem_min[0]:
            pg_value = 0
        else:
            pg_value = find_closest_value(sem_min, pg_l, sems)

        RV.append(RV_value)
        pg.append(pg_value)
        valor_p = saldo_total[i]/RV_value

        if valor_p < pg_value:
            pension.append(pg_value)
            pension_av.append(pg_value + saldo_av[i]/RV_value)
            dict_pg.append(1)
        else:
            pension.append(valor_p)
            pension_av.append(valor_p + saldo_av[i]/RV_value)
            dict_pg.append(0)

        if sems < sem_min[0]:
            dict_neg.append(1)
        else:
            dict_neg.append(0)

    tr = [x/salario_base for x in pension]
    tr_av = [x/salario_base for x in pension_av]

    saldo_av = [x - y for x,y in zip(saldo_total_av, saldo_total)]

    formatter = FuncFormatter(currency)

    if edad >= 65:
        print(saldo_total)
        print(saldo_total_av)
        print(edades)
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.4
        bar1 = ax.bar(edades, saldo_total, label='Saldo total', color='r', width=bar_width)
        if saldo_aportaciones_voluntarias != 0:
            bar2 = ax.bar(edades, [saldo_aportaciones_voluntarias], bottom=saldo_total, label='Saldo total con AV', color='c', width=bar_width)

        plt.xlim(edad - 0.5, edad + 0.5)

        plt.legend(loc = 'upper left')
        
        plt.title('Crecimiento de tu saldo', fontsize='x-large')
        plt.xlabel('Edad', fontsize='large')
        plt.ylabel('Saldo', fontsize='large')

        plt.gca().yaxis.set_major_formatter(formatter)

        plt.xticks(fontsize='medium')
        plt.yticks(fontsize='medium')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xticks(edades)
        ax.set_xticklabels(edades, fontsize='medium', ha='center')

        plt.savefig('calculator/static/calculator/crec_saldos.png')
        plt.close()

    else:

        if saldo_aportaciones_voluntarias + aportaciones_voluntarias_mensuales == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            plt.plot([], [], color ='r', label ='Saldo total')
            #plt.plot([], [], color ='c', label ='Saldo total con AV')
            
            # Implementing stackplot on data
            plt.stackplot(edades, saldo_total, baseline ='zero', colors =['r'])
            
            plt.legend(loc = 'upper left')
            
            plt.title('Crecimiento de tu saldo', fontsize='x-large')
            plt.xlabel('Edad', fontsize='large')
            plt.ylabel('Saldo', fontsize='large')

            plt.gca().yaxis.set_major_formatter(formatter)

            plt.xticks(fontsize='medium')
            plt.yticks(fontsize='medium')

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            plt.savefig('calculator/static/calculator/crec_saldos.png')
            plt.close()
        else:

            fig, ax = plt.subplots(figsize=(10, 6))
            plt.plot([], [], color ='r', label ='Saldo total')
            plt.plot([], [], color ='c', label ='Saldo total con AV')
            
            # Implementing stackplot on data
            plt.stackplot(edades, saldo_total, saldo_av, baseline ='zero', colors =['r', 'c'])
            
            plt.legend(loc = 'upper left')
            
            plt.title('Crecimiento de tu saldo', fontsize='x-large')
            plt.xlabel('Edad', fontsize='large')
            plt.ylabel('Saldo', fontsize='large')

            plt.gca().yaxis.set_major_formatter(formatter)

            plt.xticks(fontsize='medium')
            plt.yticks(fontsize='medium')

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            plt.savefig('calculator/static/calculator/crec_saldos.png')
            plt.close()

    edades_ret = edades[ret_list[0]:(ret_list[-1]+1)]

    fig, ax = plt.subplots()

    # Plot the bars
    bar_width = 0.4
    bar1 = ax.bar(edades_ret, pension, color='r', width=bar_width, label='Pensiones')
    bar2 = ax.bar(np.array(edades_ret) + bar_width, pension_av, color='c', width=bar_width, label='Pensiones con AV')

    # Set the x-ticks to be in the middle of both bars
    middle_of_bars = np.array(edades_ret) + bar_width / 2
    ax.set_xticks(middle_of_bars)
    ax.set_xticklabels(edades_ret, fontsize=18)

    # Format y-axis
    formatter = plt.FuncFormatter(lambda x, pos: f'${x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    # Ensure y-ticks are integer
    ax.set_yticks(ax.get_yticks().astype(int))

    # Set labels and title
    ax.set_xlabel('Edades', fontsize=18)
    ax.set_ylabel('Pensión', fontsize=18)
    ax.set_title('Comparación de Pensiones con y sin AV por Edad de Retiro', fontsize=22)
    plt.yticks(fontsize=18)
    ax.legend(fontsize=18)

    # Hide the top, right, left, and bottom spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    # Adjust the figure size
    fig.set_size_inches(12, 10)

    # Save the plot
    plt.savefig('calculator/static/calculator/pensiones.png')
    plt.close()

    data_pensiones = {
        'Edad de Retiro': edades_ret,
        'Pensión':[round(x,2) for x in pension],
        'Tasa de Reemplazo':[round(x*100,0) for x in tr],
        'Pensión con AV':[round(x,2) for x in pension_av],
        'Tasa de Reemplazo con AV':[round(x*100,0) for x in tr_av],
        'Negativa de Pensión': dict_neg,
        'Pensión Garantizada': dict_pg,
        #'Negativa de Pensión': [0,0,0,0,0,0],
        #'Pensión Garantizada': [0,0,0,1,0,0]
    }

    if saldo_aportaciones_voluntarias + aportaciones_voluntarias_mensuales == 0:
        indicador_av = 0
    else:
        indicador_av = 1

    extra_data = {
        'Edad_afiliado': edad,
        'Saldo_Total': round(saldo_total[-1],2),
        'Saldo_Total_AV': round(saldo_total_av[-1],2),
        'Indicador_AV': indicador_av
    }

    with open('data_pensiones.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_pensiones.keys())
        writer.writerows(zip(*data_pensiones.values()))

    print(extra_data)

    return extra_data