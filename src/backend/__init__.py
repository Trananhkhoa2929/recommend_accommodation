"""Backend Execution Module"""
from .local_search import search_accommodations
from .data_normalizer import normalize_osm_data
from .filter import filter_results
from .ranking import rank_results