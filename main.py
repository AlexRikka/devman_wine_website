from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from load_data import load_products
import datetime
import humanize
humanize.i18n.activate("ru_RU")


def render_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    company_age_delta = datetime.date.today() - \
        datetime.date(year=1920, month=1, day=1)
    company_age_delta_rus = humanize.naturaldelta(company_age_delta)

    data_path = r'data\wine3.xlsx'
    products = load_products(data_path)
    rendered_page = template.render(
        company_age=f'Уже {company_age_delta_rus} с вами',
        products_type=list(products.keys()),
        products_dict=products
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    render_template()
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
