from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from load_data import load_products
from dotenv import load_dotenv
import argparse
import datetime
import os
import humanize
humanize.i18n.activate("ru_RU")


def render_template(data_path):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    company_age_delta = datetime.date.today() - \
        datetime.date(year=1920, month=1, day=1)
    company_age_delta_rus = humanize.naturaldelta(company_age_delta)

    products = load_products(data_path)
    rendered_page = template.render(
        company_age=f'Уже {company_age_delta_rus} с вами',
        products_type=list(products.keys()),
        products_dict=products
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Run wine website')
    parser.add_argument('data_path',
                        help='path to file with products data',
                        nargs='?',
                        default=os.environ['DATA_PATH'])
    data_path = parser.parse_args().data_path
    render_template(data_path)
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
