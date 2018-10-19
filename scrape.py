from web import all_pages, get_price, get_km, get_model, get_maker, get_year
import pandas as pd


def create_table(url_link):
    prices = []
    years = []
    makers = []
    models = []
    kms = []
    soup_list = all_pages(url_link)
    for s in soup_list:
        prices.extend(get_price(s))
        years.extend(get_year(s))
        models.extend(get_model(s))
        kms.extend(get_km(s))
        makers.extend(get_maker(s))
    data = pd.DataFrame({'Price': prices, 'Made Year': years, 'Manufacture': makers, 'Model': models, 'Kilometer': kms})
    data['Made Year'] = data['Made Year'].convert_objects(convert_numeric=True)
    data = data.dropna()
    return data


if __name__ == '__main__':
    url = 'https://www.kijiji.ca/b-cars-trucks/city-of-toronto/suv+crossover-2013__2018-used/' \
          'c174l1700273a138a68a49?price=30000__80000&kilometers=10000__100000'
    df = create_table(url)
    df.to_csv('Car Scrapping.csv', sep=',')
