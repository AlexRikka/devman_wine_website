import pandas as pd


def load_products(path):
    products_df = pd.read_excel(path,
                                na_values=['None'],
                                keep_default_na=False,)
    products_df['Картинка'] = 'images/' + products_df['Картинка']
    products_df.set_index(keys=['Категория'], drop=True, inplace=True)
    products_dict = {}
    for idx in products_df.index.unique():
        products_dict[idx] = products_df.loc[idx].to_dict('records')
    return products_dict
