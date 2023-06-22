from dtcc_model import City

from . import summarize, enrich

City.add_processors(summarize)
City.add_processors(enrich)
