from dtcc_model import CityModel

from . import summerize, enrich

CityModel.add_processors(summerize)
CityModel.add_processors(enrich)
