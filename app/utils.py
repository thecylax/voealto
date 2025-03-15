import datetime
import os
from typing import Dict

import cairosvg
from django.conf import settings
from django.template.loader import get_template
from jinja2 import Environment, FileSystemLoader


def format_date(value: datetime.date):
    if value and isinstance(value, datetime.date):
        return value.strftime('%d/%m/%Y')
    return "--/--/----"

def format_time(value, format="%H:%M"):
    """Formata um objeto de tempo para exibir apenas horas e minutos."""
    if value:
        return value.strftime(format)
    return "--:--"  # Valor padrão para campos NULL

def format_decimal(value):
    """Formata um valor decimal para usar vírgula como separador."""
    if value is not None:
        return f"{value:.2f}".replace(".", ",")
    return "0,00"  # Valor padrão para campos NULL

def render_template(data: Dict, context):
    # Carregar o template
    template_dir = os.path.join(settings.BASE_DIR, 'app/templates/pdf')
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['format_date'] = format_date
    env.filters['format_time'] = format_time
    env.filters['format_decimal'] = format_decimal
    template = env.get_template('template_v2_jinja.svg')

    offset = 31.76
    if isinstance(context, list):
        total_value = sum(float(i.ticket_value) for i in context[0].items.all())
    else:
        total_value = sum(float(i.ticket_value) for i in context)
    last_y = 102.04986 + offset * (len(context) - 1)
    local_tz = datetime.datetime.now().astimezone().tzinfo
    local_date = data['date'].astimezone(local_tz)
    general = {
        'offset': offset,
        'total_value': total_value,
        'today': local_date.strftime('%d/%m/%Y %H:%M:%S'),
        'last_y': last_y + 35.30,
    }

    # Max. y == 229.04987 -> max y do box ou len(context) == 5

    # Renderizar o template com os dados
    if isinstance(context, list):
        ctx = [i.items.all() for i in context]
        output_svg = template.render(context=[i[0] for i in ctx], client=data['client'], general=general)
    else:
        output_svg = template.render(context=context, client=data['client'], general=general)

    # Salvar o SVG renderizado em um arquivo
    output_file = os.path.join(settings.BASE_DIR, 'app/static/output/output.svg')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_svg)

    print("SVG gerado com sucesso!")

    pdf_file = os.path.join(settings.BASE_DIR, 'app/static/output/resultado.pdf')
    cairosvg.svg2pdf(url=output_file, write_to=pdf_file)

    return output_svg, pdf_file