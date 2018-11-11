import requests
from beer_and_styles import Beer, Style, Base
from sqlalchemy.orm import sessionmaker
import sqlalchemy


class GetBeerData:
    def get_beer_data(self):
        pages = range(1,24)
        full_pages = []
        for i in pages:
            r = requests.get(f'http://api.brewerydb.com/v2/beers?key=f684318419e2e8da8014c50bb077ddc6&p={i}')
            data = r.json()['data']
            full_pages.append(data)
        all_pages = []
        list(map(all_pages.extend, full_pages))
        return all_pages

class BeerBuilder:
    def run(self):
        beer_data = GetBeerData()
        beer_data.get_beer_data()
        beers = []
        for beer in beer_data.get_beer_data():
            try:
                beer['style']
                try:
                    beer['style']['shortName']
                    try:
                        #everything
                        each_beer = Beer(name = beer['name'],
                        nameDisplay = beer['nameDisplay'], description = beer['description'],
                        abv = beer['abv'], ibu = beer['ibu'], isOrganic = beer['isOrganic'],
                        foodPairings = beer['foodPairings'], style = beer['style']['name'])
                        each_beer.style_shortName = session.query(Style).filter(Style.shortName == beer['style']['shortName'])

                    except:
                        each_beer = Beer(name = beer['name'],
                        nameDisplay = beer['nameDisplay'], isOrganic = beer['isOrganic'],
                        style = beer['style']['name'])
                        each_beer.style_shortName = session.query(Style).filter(Style.shortName == beer['style']['shortName'])
                except:
                    pass
            except:
                pass
            beers.append(each_beer)
        return beers


class StyleBuilder:
    def run(self):
        styler = requests.get('http://api.brewerydb.com/v2/styles?key=f684318419e2e8da8014c50bb077ddc6&p=1')
        style_data = styler.json()['data']
        beer_styles = []
        for style in style_data:
            try:
                each_style = Style(name = style['name'], category = style['category']['name'], description = style['description'], ibuMin = style['ibuMin'], ibuMax = style['ibuMax'], abvMin = style['abvMin'], abvMax = style['abvMax'])
            except:
                each_style = Style(name = style['name'], category = style['category']['name'])
            beer_styles.append(each_style)
        return beer_styles


engine = sqlalchemy.create_engine('sqlite:///beers.db', echo=True)
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

x = StyleBuilder()
session.add_all(x.run())
session.commit()

y = BeerBuilder()
session.add_all(y.run())
session.commit()