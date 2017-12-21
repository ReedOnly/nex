import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import datetime as dt

with open('history_271017_obs.csv') as fp:
    df = pd.read_csv(fp, skiprows=[0, 1, 2], nrows=10179)

df['datetime'] = [dt.datetime.strptime(x, '%d/%m/%Y') for x in df.DATE]
wells = [df[df.WELL.isin([well])] for well in set(df.WELL)]
for well in wells: well = well.reset_index(drop=True)


# wells is the initial dataFrame and interp_wells the final interpolated
interp_wells = []
for well in wells:
    well = well.reset_index(drop=True)
    new_df = pd.DataFrame()
    #nex_timesteps is the input timesteps we want to sample data to
    nex_timesteps = [well.datetime[0] + dt.timedelta(hours=x) for x in range(0, 696, 6)]
    nex_timesteps_epoch = [x.timestamp() for x in nex_timesteps]
    new_df['DATE'] = nex_timesteps
    new_df['WELL'] = well['WELL']
    orig_ts_epoch = [x.timestamp() for x in well.datetime]
    for column in well:
        if column == 'DATE' or column == 'datetime' or column == 'WELL': continue
        # zero order spline interpolation will behave like a step function
        f = interpolate.interp1d(orig_ts_epoch, well[column], kind='zero')
        new_df[column] = f(nex_timesteps_epoch)
    interp_wells.append(new_df)


###########################################################
## Small example with step interpolation
##########################################################
a08 = wells[-1]
small = a08[:30]

timesteps = [small.datetime[0] + dt.timedelta(hours=x) for x in range(0, 700, 6)]
timesteps_e = [x.timestamp() for x in timesteps]
orig_ts_e = [x.timestamp() for x in small.datetime]

f = interpolate.interp1d(orig_ts_e, small.COP, kind='zero')
intpol_y = f(timesteps_e)

plt.plot(orig_ts_e, small.COP, 'rx')
plt.plot(timesteps_e, intpol_y, 'b')
plt.show()

################################################################
