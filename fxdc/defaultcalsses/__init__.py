from .pythondefaults import load as pythondefaults_load
try:
    from .numpydefaults import load as numpydefaults_load
except ImportError:
    numpydefaults_load = None
try:
    from .pandasdefaults import load as pandasdefaults_load
except ImportError:
    pandasdefaults_load = None
from .datetimedefaults import load as datetime_load


def load_default_classes():
    pythondefaults_load()
    if numpydefaults_load:
        numpydefaults_load()
    if pandasdefaults_load:
        pandasdefaults_load()
    datetime_load()