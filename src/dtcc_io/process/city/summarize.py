from dtcc_model import Landuse, Building
from collections import defaultdict
from statistics import mean, median, stdev


def summarize_landuse(city, print_summary=True):
    landuse_summaries = defaultdict(float)
    for lu in city.landuse:
        landuse_summaries[lu.landuse.name] += lu.area
    if print_summary:
        print("Landuse summary:")
        for k, v in landuse_summaries.items():
            print(f"  {k}: {v:.0f} m²")
    return landuse_summaries


def summarize_buildings(city, print_summary=True):
    building_footprint_areas = [b.area for b in city.buildings]
    summary = {
        "number": len(building_footprint_areas),
        "total_area": sum(building_footprint_areas),
        "average_area": mean(building_footprint_areas),
        "median_area": median(building_footprint_areas),
        "std_area": stdev(building_footprint_areas),
    }
    if print_summary:
        print("Building summary:")
        print(f"  Number of buildings: {len(building_footprint_areas)}")
        print(f"  Total footprint area: {sum(building_footprint_areas):.0f} m²")
        print(f"  Average footprint area: {mean(building_footprint_areas):.0f} m²")
        print(f"  Median footprint area: {median(building_footprint_areas):.0f} m²")
        print(
            f"  Standard deviation footprint area: {stdev(building_footprint_areas):.0f} m²"
        )
    return summary
