import pandas as pd
import numpy as np
import scipy
import os
import sys
import collections
import datetime
import os.path


pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 500)



class Triangle(pd.DataFrame):
    """
    Revised and updated Loss Triangle class.
    """
    def __init__(self, data, origin=None, dev=None, value=None, inc=True):
            """Transform a dataset into a loss triangle."""

        # keep only necessary fields, and aggregate by origin & dev =>

        dataset = data[[origin, dev, value]]
        dataset = data.groupby([origin, dev], as_index=False).sum()

        # transform dataset into incremental loss triangle =>
        tri = dataset.pivot(index=origin, columns=dev).rename_axis(None)
        tri.columns = tri.columns.droplevel(0)

        pd.DataFrame.__init__(self, tri)
        self._tri = tri
        self.origin = origin
        self.value = value
        self.dev = dev
        self.inc = inc

        # properties
        self._latest_diag = None
        self.dev_periods  = None
        self._origin_yrs = None



    @property
    def latest_diag(self):
        """
        Return latest diagonal.
        """
        if self._latest_diag is None:
            self._latest_diag = \
                [self._tri.loc[self._tri[i].last_valid_index(),i]
                     for i in self._tri]
        return(self._latest_diag)



    @property
    def dev_periods(self):
        """
        Return Triangle development periods.
        """
        if self._dev_periods is None:
            self._dev_periods = np.array(self._tri.columns)
        return (self._dev_periods)



    @property
    def origin_yrs(self):
        """
        Return Triangle origin years.
        """
        if self._origin_yrs is None:
            self._origin_yrs = np.array(self._tri.index)
        return(self._origin_yrs)





ff = "U:\\Repos\\trikit\\datasets\\RAA.csv"
raa = pd.read_csv(ff)
t = Triangle(raa, origin='ORIGIN', dev='DEV', value='VALUE')


print(t.latest_diag)
print(t.dev_periods)
print(t.origin_yrs)

