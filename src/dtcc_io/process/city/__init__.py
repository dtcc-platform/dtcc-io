from dtcc_model import City

from . import summarize, enrich

City.add_methods(summarize)
City.add_methods(enrich)
