import pynex
import pandas as pd

def load(filename):
    raw = pynex.load(filename)
    df = pd.DataFrame([{
        'timestep'     : d.timestep,
        'time'         : d.time,
        'classname'    : d.classname,
        'instancename' : d.instancename,
        'varname'      : d.varname,
        'value'        : d.value,
    } for d in raw._data])
    return df
