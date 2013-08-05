from generator import ServiceGenerator, loader
from mapping import ServiceMapper

def factory(**opts):
    return ServiceGenerator(**opts)
