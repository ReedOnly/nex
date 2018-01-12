import datetime
from .pynex import load as _load
import pandas


def load(filename):
    """Load a binary format nexus plot file into a pandas DataFrame

    Args:
        filename (str): Path to a binary format nexus plot file.
    :rtype: DataFrame

    """

    raw = _load(filename)
    df = pandas.DataFrame([{
        'timestep': d.timestep,
        'time': d.time,
        'classname': d.classname,
        'instancename': d.instancename,
        'varname': d.varname,
        'value': d.value,
    } for d in raw._data])
    df.start_date = datetime.datetime(
        year=raw._header.year,
        month=raw._header.month,
        day=raw._header.day,
    )
    df.grid_dimensions = (raw._header.nx, raw._header.ny, raw._header.nz)
    df.unit_system = raw._header.unit_system.name
    return df


def nex2ecl(plt):
    pass