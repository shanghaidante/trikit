import pandas as pd
import numpy as np
import itertools
import collections
import csv
import os
import os.path
import pdb
import logging
import sys


# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 500)
# np.set_printoptions(precision=5, suppress=True)


# =============================================================================
# _BaseTriangle class                                                         |
# =============================================================================
class _BaseTriangle(pd.DataFrame):

    def __init__(self, data=None, **kwargs):
        """
        Transform a dataset into a triangle.
        """
        origin  = kwargs.get('origin' ,None)
        dev     = kwargs.get('dev'    ,None)
        value   = kwargs.get('value'  ,None)
        trisize = kwargs.get('trisize',None)

        if data is None:

            try:
                tri = pd.DataFrame(columns=range(1, trisize+1),index=range(trisize))

            except (TypeError, AttributeError) as e:
                tri = pd.DataFrame(columns=[], index=[])

        else: tri = data

        super().__init__(tri)


        # properties
        self._latest_diag = None
        self._dev_periods = None
        self._origin_yrs  = None

        # attributes
        self.origin  = origin
        self.dev     = dev
        self.value   = value
        self.trisize = trisize



    @property
    def latest_diag(self) -> np.ndarray:
        """
        Return latest diagonal as numpy array.
        """
        if self._latest_diag is None:

            if self.isnull().values.all():
                self._latest_diag = \
                    np.full(self.shape[0], np.NaN)
            else:
                self._latest_diag = \
                    np.array([self.loc[self[i].last_valid_index(), i]
                        for i in self])

        return(self._latest_diag)



    @property
    def dev_periods(self) -> np.ndarray:
        """
        Return Triangle development periods as numpy array.
        """
        if self._dev_periods is None:
            self._dev_periods = self.columns
        return (np.array(self._dev_periods))



    @property
    def origin_yrs(self) -> np.ndarray:
        """
        Return Triangle origin years as numpy array.
        """
        if self._origin_yrs is None:
            self._origin_yrs = np.array(self.index)
        return (np.array(self._origin_yrs))



    def get_origin(self, origin_yr: int) -> np.ndarray:
        """
        Return the row corresponding to origin_yr as a numpy array.
        If origin_yr not in origin_yrs list, raise KeyError.
        """
        if origin_yr not in self.origin_yrs:
            raise KeyError("Invalid origin year specified.")
        return (self.loc[origin_yr].values)



    def get_dev(self, dev_period: int) -> np.ndarray:
        """
        Return the column corresponding to dev_period as a numpy array.
        f dev_period not in dev_periods list, raise KeyError.
        """
        if dev_period not in self.dev_periods:
            raise KeyError("Invalid development period specified.")
        return (self[dev_period].values)



    def save_triangle(self, fname, format="csv"):
        """
        Write triangle to .csv or .xlsx file.
        """
        self.to_csv(fname, sep=",", header=True, index=True)






# =============================================================================
# _IncrTriangle class                                                          |
# =============================================================================
class _IncrTriangle(_BaseTriangle):

    def __init__(self, data=None, **kwargs):

        origin  = kwargs.get('origin' ,None)
        dev     = kwargs.get('dev'    ,None)
        value   = kwargs.get('value'  ,None)
        trisize = kwargs.get('trisize',None)
        tri     = None

        if data is not None:

            if isinstance(data, _CumTriangle):

                tri = pd.DataFrame().reindex_like(data)
                tri.iloc[:,0] = data.iloc[:,0]
                tri = tri.iloc[:,[0]]
                tri = pd.merge(
                        tri, data.diff(axis=1).iloc[:,1:],
                        right_index=True,
                        left_index=True
                        )

            elif set(['origin','dev','value']).issubset(kwargs.keys()):

                try:
                    tri = data[[origin, dev, value]]
                    tri = tri.groupby([origin, dev], as_index=False).sum()
                    tri = tri.pivot(index=origin, columns=dev).rename_axis(None)
                    tri.columns = tri.columns.droplevel(0)

                except KeyError:
                    print("One or more fields are not present in supplied dataset.")

            else: # Check if fields are `ORIGIN`, `DEV`, `VALUE`

                try:
                    tri = data[['ORIGIN', 'DEV', 'VALUE']]
                    tri = tri.groupby(['ORIGIN', 'DEV'], as_index=False).sum()
                    tri = tri.pivot(index='ORIGIN', columns='DEV').rename_axis(None)
                    tri.columns = tri.columns.droplevel(0)

                except KeyError:
                    print("One or more fields are not present in supplied dataset.")


        #_BaseTriangle.__init__(self, tri, **kwargs)
        super().__init__(tri, **kwargs)

        # for attribute, value in kwargs.items():
        #     setattr(self, attribute, value)

        self.tritype = "incremental"







# =============================================================================
# _CumTriangle class                  # tri = tri.cumsum(axis=1)              |
# =============================================================================
class _CumTriangle(_BaseTriangle):
    """
    Create cumulative triangle instance.
    """
    _nbr_periods = [3, 5, 7]

    def __init__(self, data=None, **kwargs):
        """
        Cumulative triangle initializer.

        """
        origin  = kwargs.get('origin' ,None)
        dev     = kwargs.get('dev'    ,None)
        value   = kwargs.get('value'  ,None)
        trisize = kwargs.get('trisize',None)
        tri     = None

        if data is not None:

            if isinstance(data, _IncrTriangle):

                tri = data.cumsum(axis=1)

            elif set(['origin','dev','value']).issubset(kwargs.keys()):

                try:

                    tri = data[[origin, dev, value]]
                    tri = tri.groupby([origin, dev], as_index=False).sum()
                    tri = tri.pivot(index=origin, columns=dev).rename_axis(None)
                    tri.columns = tri.columns.droplevel(0)
                    tri = tri.cumsum(axis=1)

                except KeyError:

                    print("One or more fields are not present in supplied dataset.")

            else: # Check if fields are `ORIGIN`, `DEV`, `VALUE`

                try:
                    tri = data[['ORIGIN', 'DEV', 'VALUE']]
                    tri = tri.groupby(['ORIGIN', 'DEV'], as_index=False).sum()
                    tri = tri.pivot(index='ORIGIN', columns='DEV').rename_axis(None)
                    tri.columns = tri.columns.droplevel(0)

                except KeyError:
                    print("One or more fields are not present in supplied dataset.")


        # _BaseTriangle.__init__(self, tri, **kwargs)
        super().__init__(tri, **kwargs)

        # for attribute, value in kwargs.items():
        #     setattr(self, attribute, value)

        # self.origin  = origin
        # self.value   = value
        # self.dev     = dev
        self.tritype = "cumulative"

        # properties
        self._a2a      = None
        self._a2a_avgs = None


    @staticmethod
    def _geometric(vals, weights=None):
        """
        Return the geometric average of the elements of vals.
        """
        if len(vals) == 0: return (None)
        vals = list(vals)
        return (np.prod(vals) ** (1 / len(vals)))



    @staticmethod
    def _simple(vals, weights=None):
        """
        Return the simple average of elements of vals.
        """
        if len(vals) == 0: return (None)
        return (sum(i for i in vals) / len(vals))



    @staticmethod
    def _medial(vals, weights=None):
        """
        Return the medial average of elements in vals. Medial
        average eliminates the min and max values, then returns
        the arithmetic average of the remaining items.
        """
        vals = list(vals)
        if len(vals) == 0: avg = None
        if len(vals) == 1:
            avg = vals[0]
        elif len(vals) == 2:
            avg = sum(vals) / len(vals)
        else:
            max_indx = vals.index(max(vals))
            vals.remove(vals[max_indx])
            min_indx = vals.index(min(vals))
            vals.remove(vals[min_indx])
            avg = sum(vals) / len(vals)
        return (avg)



    @property
    def a2a(self):
        """
        Return pandas DataFrame of age-to-age factors.
        Will have 1 less row and 1 less column than self.
        """
        if self._a2a is None:
            if self.isnull().values.all(): return(None)
            self._a2a = _BaseTriangle(trisize=len(self.columns)-1)
            self._a2a.index = self.index[:-1]

            for i in range(len(self._a2a.columns)):

                a2ahdr = str(self.columns[i]) + "-" + str(self.columns[i+1])
                self._a2a.rename(columns={self._a2a.columns[i]: a2ahdr}, inplace=True)


            # calculate link ratios
            for i in range(len(self._a2a.index)):

                iterindx = self._a2a.index[i]

                for j in range(len(self._a2a.columns)):

                    itercol = self._a2a.columns[j]
                    itertri_1, itertri_2 = self.iloc[i, j], self.iloc[i, j + 1]

                    if np.isnan(itertri_1) or itertri_1 < 1:
                        itera2a = np.nan

                    elif np.isnan(itertri_2) or itertri_2 < 1:
                        itera2a = np.nan

                    else:
                        itera2a = (itertri_2/itertri_1)

                    self._a2a.set_value(iterindx, itercol, itera2a)

        return (self._a2a)



    @property
    def a2a_avgs(self):
        """
        Return a DataFrame of various age-to-age averages.
        """
        if self._a2a_avgs is not None: return(self._a2a_avgs)

        indxstrs = list()

        # Create lookup table for average functions.
        avgfuncs = {
            'simple'   :self._simple,
            'geometric':self._geometric,
            'medial'   :self._medial,
            'weighted' :None
            }

        # Remove `0` entry, and add as last element of list.
        self._nbr_periods = list(set(self._nbr_periods))
        self._nbr_periods.sort()
        self._nbr_periods.append(0)
        a2a_avg_lst = list(itertools.product(avgfuncs.keys(),self._nbr_periods))


        for i in a2a_avg_lst:
            iteravg, iterdur = i[0], i[1]
            iterstr = "all-" + str(iteravg) if iterdur==0 \
                          else str(iterdur) + "-" + str(iteravg)
            indxstrs.append(iterstr)

        indx = sorted(a2a_avg_lst, key=lambda x: x[1])
        self._a2a_avgs = pd.DataFrame(
                                index=indxstrs,
                                columns=self.a2a.columns
                                )

        for a in enumerate(a2a_avg_lst):

            duration, avgtype, indxpos = a[1][1], a[1][0], a[0]
            indxstr, iterfunc = indxstrs[indxpos], avgfuncs[avgtype]

            for col in range(self.a2a.shape[1]):

                itercol, colstr = self.a2a.iloc[:, col], self.a2a.columns[col]

                if avgtype=='weighted':

                    t_ic_1, t_ic_2 = self.iloc[:, col], self.iloc[:, (col + 1)]

                    # Find first NaN value in t_ic_2.
                    first_nan_year  = t_ic_2.index[t_ic_2.apply(np.isnan)][0]
                    first_nan_indx  = t_ic_2.index.searchsorted(first_nan_year)
                    final_cell_indx = first_nan_indx

                    if duration==0:
                        first_cell_indx = 0

                    else:
                        first_cell_indx = (final_cell_indx-duration) if \
                                          (final_cell_indx-duration)>=0 else 0

                    # Divide sum of t_ic_2 by t_ic_1.
                    ic_2     = t_ic_2[first_cell_indx:final_cell_indx]
                    ic_1     = t_ic_1[first_cell_indx:final_cell_indx]
                    sum_ic_2 = t_ic_2[first_cell_indx:final_cell_indx].sum()
                    sum_ic_1 = t_ic_1[first_cell_indx:final_cell_indx].sum()

                    try:

                        iteravg = (sum_ic_2/sum_ic_1)

                    except ZeroDivisionError:

                        iteravg = np.Inf


                else: # avgtype in ('simple', 'geometric', 'medial')

                    # find index of first row with NaN
                    if any(itercol.map(lambda x: np.isnan(x))):

                        first_nan_year = itercol.index[
                                            itercol.apply(lambda x: np.isnan(x))][0]

                        first_nan_indx = itercol.index.searchsorted(first_nan_year)
                        final_cell_indx = first_nan_indx

                        if duration==0:
                            first_cell_indx = 0

                        else:
                            first_cell_indx = (final_cell_indx-duration) if \
                                              (final_cell_indx-duration)>=0 else 0

                    else:

                        # when itercol has 0 NaNs
                        final_cell_indx = len(itercol)
                        first_cell_indx = 0 if duration==0 else (final_cell_indx-duration)

                    try:

                        iteravg = iterfunc(itercol[first_cell_indx:final_cell_indx])

                    except ZeroDivisionError:

                        iteravg = np.Inf

                self._a2a_avgs.loc[indxstr, colstr] = iteravg

        return(self._a2a_avgs)




    def plot(self, file=None):
        """
        Visualize triangle development patterns. If file is
        given, save plot to that location.
        """
        pass








class _Triangle:

    def __init__(self, data, **kwargs):
        #
        # self.incr = incr
        # self.cum = cum

        origin  = kwargs.get('origin' ,None)
        dev     = kwargs.get('dev'    ,None)
        value   = kwargs.get('value'  ,None)
        trisize = kwargs.get('trisize',None)

        self.cum  = _CumTriangle(data,origin=origin,dev=dev,value=value)
        self.incr = _IncrTriangle(data,origin=origin,dev=dev,value=value)
        self.cumulative  = self.cum
        self.incremental = self.incr

