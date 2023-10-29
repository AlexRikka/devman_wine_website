from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
import datetime
import humanize
humanize.i18n.activate("ru_RU")

products_df = pd.read_excel(r'data\wine3.xlsx',
                            na_values=['None'],
                            keep_default_na=False,)
products_df['Картинка'] = 'images/'+products_df['Картинка']
products_df.set_index(keys=['Категория'], drop=True, inplace=True)
products_dict = {}
for idx in products_df.index.unique():
    products_dict[idx] = products_df.loc[idx].to_dict('records')

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

company_age_delta = datetime.date.today() - \
    datetime.date(year=1920, month=1, day=1)
company_age_delta_rus = humanize.naturaldelta(company_age_delta)

rendered_page = template.render(
    company_age=f'Уже {company_age_delta_rus} с вами',
    products_type=list(products_dict.keys()),
    products_dict=products_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
