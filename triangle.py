import pandas as pd
import numpy as np
import itertools
import csv
import os
import os.path
import pdb
import logging



__all__ = ["BaseTriangle", "_Incremental", "_Cumulative"]




logging.basicConfig(
        filename="U:/Repos/trikit/Logs/trikitLogs.txt",
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )




class Triangles:
    """
    Transform an input dataset into an object containing
    incremental and cumulative triangles attributes.
    """
    def __init__(self, data, sep=None,
                    origin=None, dev=None, val=None, inccol=None, cumcol=None):

        self.data = data
        self.sep = sep
        self.origin = origin
        self.dev = dev
        self.value = value
        self.incremental = incremental



# =============================================================================
# BaseTriangle class                                                          |
# =============================================================================
class _BaseTriangle(pd.DataFrame):
    """
        The Triangle class transforms tabular data into an incremental loss
        triangle, with development periods running horizontally (increasing
        from left to right), and with origin period (typically `year`) running
        vertically (increasing from top to bottom). To illustrate:

                    Increasing Development Period =====>

                    Typically:
                        `1` =>  0-12 Months
                        `2` => 12-24 Months
                        `3` => 24-36 Months, etc...

                   ==============================================
      Increasing   |****|   1   |   2   |   3   |   4   |   5   |
        Origin     ==============================================
         Year      |2012| 1065    2793    1875    2211    1287  |
          ||       |2013|  942    1232    1179    1514     NaN  |
          ||       |2014| 1334    1887    1665     NaN     NaN  |
          ||       |2015| 1774    2173     NaN     NaN     NaN  |
          \/       |2016| 2229     NaN     NaN     NaN     NaN  |
                   ==============================================

          Assuming the sample triangle contains incremental paid losses, the
        1875 dollar amount in cell (2012, 3) represents losses paid between
        24-36 months after the claim was reported (sometime in 2014).

          In order to create an instance of the Triangle class, it is necessary
        to provide, at a minimum, the fieldnames from the dataset that
        correspond to Loss Year (the `origin` argument), Development Period
        (the `dev` argument) and Loss Amount (the `value` argument). Note that
        **kwargs represents a collection of keyword arguments that permit
        specifying multiple fields in the referenced dataset, so that triangles
        can be generated for multiple types of loss simultaneously: For
        example, claim datasets typically contain reported claims, paid claims
        and ALAE, in addition to paid and reported claim counts. It is possible
        to pass to the Triangle class constuctor a dictionary which maps the
        fieldnames specific to the dataset to a corresponding user-defined
        handle. The only requirement is that 'origin' correspond to the key for
        loss year, and 'dev' corresponds to the key for development period.

          If only a single loss triangle needs to be created (corresponding to
        losses falling under a single column header in the provided dataset),
        simply pass this fieldname to the `value` parameter in the Triangle
        class constructor. What follows are examples demonstrating both
        methods of instantiation: Creating a single loss triangle, with the
        field of interest passed as an argument to `value`, and creating
        multiple triangles, with instantiation details contained in a
        dictionary of key-value pairs which are passed to the Triangle
        constructor:


        ===========================================================================
        | Example I  (using origin, dev and value keyword arguments)              |
        ===========================================================================

            Assume our dataset can be found here:

                * Dataset = "E:\\Datasets\\Q3_Claims.csv"

            Within `Q3_Claims.csv`, the fields of interest are:

                * LOSS_YR            => (corresponds to `origin` in Triangle class)
                * DEV_PERIOD         => (corresponds to `dev`    in Triangle class)
                * INCRD_LOSS_NET_DED => (corresponds to `value`  in Triangle class)

            Therefore, the Example I Triangle class instantiation would be =>

            tri = Triangle('E:\\Datasets\\Q3_Claims.csv',
                           origin='LOSS_YR',
                           dev='DEV_PERIOD',
                           value='INCRD_LOSS_NET_DED')



        ===========================================================================
        | Example II (passing key-value pairs dict to generate several triangles) |
        ===========================================================================

            Assume our dataset can be found here:

                * Dataset = "E:\\Datasets\\Q3_Claims.csv"

            But for this example, we're interested in generating loss triangles
            for ALAE, reported losses and paid losses, in addition to paid claim
            counts. Since multiple fieldnames are required, the keyword arguments
            will be ignored, and all Triangle inputs (with the exception of fname)
            will be read from the passed-in dictionary of key-value pairs:

                * LOSS_YR            => ('origin'      as dict key)     ***required***
                * DEV_PERIOD         => ('dev'         as dict key)     ***required***
                * INCRD_LOSS_NET_DED => ('incrd_loss'  as dict key) ***user-defined***
                * PAID_LOSS_NET_DED  => ('paid_loss'   as dict key) ***user-defined***
                * ALAE               => ('alae'        as dict key) ***user-defined***
                * PAID_FREQ          => ('paid_counts' as dict key) ***user-defined***

            The name given to the dictionary of key-value pairs is also
            arbitrary: Here, it will be identified as `argvs`. In short,
            `argvs` maps fieldnames from the dataset to the names
            that will be used in identifying each triangle. To construct
            `argvs`:

                 argvs = {'origin'       :'LOSS_YR',
                          'dev'          :'DEV_PERIOD',
                          'paid_loss'    :'PAID_LOSS_NET_DED',
                          'alae'         :'ALAE',
                          'incurred_loss':'INCRD_LOSS_NET_DED',
                          'paid_counts'  :'PAID_FREQ'}

            Thus, the instantiation for Example II is:

                tris = Triangle('E:/Datasets/Q3_Claims.csv', **argvs)

            `tris` will be a dict containing  incremental and cumulative loss
            triangles for paid losses, incurred losses, ALAE and paid counts.
            To access a given loss triangle, call the tris dict with the name
            used above. To access the 'paid_loss' triangle, enter:

                tris['paid_loss']

            Similiarily, to access any of the other triangles:

                tris['incurred_loss']   # for incurred losses
                tris['alae']            # for ALAE
                tris['paid_counts']     # for paid counts


        ===========================================================================
        | Parameter Description                                                   |
        ===========================================================================

        fname:      The absolute filepath associated with the dataset of interest.

        origin:     Defaults to None. Represents the year in which a given claim
                    or collection of claims
    """
    def __init__(self, data, sep=None, origin=None, dev=None, value=None, inc=True):
        """Transform a dataset into a loss triangle."""
        if isinstance(data, pd.DataFrame): dataset = data
        elif os.path.isfile(data):    # read delimited file into DataFrame
            if sep is None:           # use csv module to identify delimiter
                with open(data, "r") as f:
                    hdr = next(f).replace(" ", "")
                    snfr = csv.Sniffer()
                    dialect  = snfr.sniff(hdr)
                    sep = dialect.delimiter

            dataset = pd.read_table(data, sep=sep)

        # keep only necessary fields, and aggregate by origin & dev =>
        dataset = dataset[[origin, dev, value]]
        dataset = dataset.groupby([origin, dev], as_index=False).sum()

        # transform dataset into incremental loss triangle =>
        tri = dataset.pivot(index=origin, columns=dev).rename_axis(None)
        tri.columns = tri.columns.droplevel(0)

        pd.DataFrame.__init__(self, tri)
        self._triangle = tri
        self._iscumulative = None
        self._latest_diagonal = None
        self._dev_periods = None
        self._origin_yrs = None
        self.tri_field = None
        self.tri_desc = None
        self.tritype = None
        self.origin = origin
        self.value = value
        self.data = data
        self.dev = dev
        self.sep = sep
        #self.inc = inc



    @property
    def dev_periods(self) -> list:
        """
        Return the development periods associated with triangle.
        """
        if self._dev_periods is None:
            self._dev_periods = sorted(self._triangle.columns.tolist())
        return(self._dev_periods)



    @property
    def origin_yrs(self) -> list:
        """
        Return list of origin years for triangle.
        """
        if self._origin_yrs is None:
            self._origin_yrs = sorted(self.index.tolist())
        return(self._origin_yrs)



    @property
    def latest_diagonal(self) -> pd.DataFrame:
        """
        Return triangle's latest diagonal as a pandas DataFrame.
        """
        if self._latest_diagonal is None:
            ncols = len(self._triangle.columns)
            nrows = len(self._triangle.index)
            ldiagl = list()
            colpos = 0

            for i in range(nrows):
                i_i = nrows - i - 1
                ldiagl.append(self._triangle.iloc[i_i, colpos])
                colpos+=1

            # combine self.columns with ldiag into pandas DataFrame =>
            self._latest_diagonal = pd.DataFrame(
                                        pd.Series(
                                            ldiagl,
                                            index=list(self._triangle.columns))).transpose()
        return(self._latest_diagonal)



    def colsum(self, column, use_labels=True) -> float:
        """
        Return the sum of cells in `column`. If `use_labels` is True (default),
        cells are referenced by column label; otherwise cells are referenced
        by position offset. If `use_labels` is False, `column` must be an
        integer.
        """
        if use_labels:
            if column not in self.dev_periods:
                raise KeyError("Invalid column specified.")
            cs = self._triangle[column].sum()

        else:
            if not isinstance(column, int):
                raise TypeError("`column` must be type <'int'> when `use_col_labels` is False.")

            # use index offset to identify column =>
            if column >= len(self.dev_periods):
                raise IndexError("Development period referenced is invalid.")
            cs = self._triangle.iloc[:, column].sum()
        return(cs)



    def rowsum(self, row, use_labels=True):
        """
        Return the sum of cells in `row`. If `use_labels` is True (default),
        cells are referenced by index label; otherwise cells are referenced
        y index offset. If `use_labels` is False, `row` must be an integer.
        """
        if use_labels:
            if row not in self._triangle.index:
                raise KeyError("Invalid row specified.")
            rs = self._triangle.loc[row,].sum()

        else:
            if not isinstance(row, int):
                raise TypeError(
                    "`row` must be <'int'> when `use_index_labels` is False."
                    )

            # use index offset to identify row =>
            if row >= len(self.index):
                raise IndexError("Referenced origin year invalid.")
            rs = self._triangle.iloc[row,].sum()
        return(rs)




    def get_origin(self, origin_yr:int) -> pd.DataFrame:
        """
        Return the row corresponding to origin_yr as a pandas DataFrame. If
        origin_yr not in origin_yrs list, raise KeyError.
        """
        if origin_yr not in self.origin_yrs:
            raise KeyError("Invalid origin year specified.")
        else:
            return(self._triangle.loc[[origin_yr]])



    def get_dev(self, dev_period):
        """
        Return the column corresponding to dev_period as a pandas DataFrame.
        f dev_period not in dev_periods list, raise KeyError.
        """
        if dev_period not in self.dev_periods:
            raise KeyError("Invalid development period specified.")
        else:
            return(self._triangle[[dev_period]])




    def save_triangle(self, fname, format="csv"):
        """
        Write triangle to .csv or .xlsx file.
        """
        self._triangle.to_csv(fname, sep=",", header=True, index=True)
        pass



    def __repr__(self):
        return(
            self._triangle.applymap(lambda x: 0 if x < 1 else x).to_string()
            )



# =============================================================================
# Incremental Triangle Class                                                  |
# =============================================================================
class Incremental(_BaseTriangle):
    """
    The Incremental class is a replication of the BaseTriangle class,
    included so that `Incremental` and `Cumulative` would each be subclasses
    of a single BaseTriangle class. Coerces cell values less than $1 to $1.
    """
    def __init__(self, data, sep=None, origin=None, dev=None, value=None):
        BaseTriangle.__init__(self, data, sep, origin, dev, value)
        hdr  = list(self._triangle.columns.values)
        indx = list(self._triangle.index.values)

        for i in range(len(indx)):

            iteridx = indx[i]
            lastidx = len(indx)-1-i

            for j in range(len(hdr)):

                iterhdr = hdr[j]

                if j <= lastidx:

                    if self._triangle.iloc[i, j]<1:
                        self._triangle.set_value(iteridx, iterhdr, 1.)


    @property
    def a2a(self):
        """Return pandas DataFrame of age-to-age factors based on triangle."""
        raise AttributeError(
            "Unable to calculate Age-to-Age factors for incremental triangle."
            )





# =============================================================================
# Cumulative Triangle Class                                                   |
# =============================================================================
class Cumulative(_BaseTriangle):
    """
    Cumulative Triangle class.
    """
    def __init__(self, data, sep=None, origin=None, dev=None, value=None):
        BaseTriangle.__init__(self, data, sep, origin, dev, value)
        self._a2a = None
        self._udf = None
        self._avg_types = ['simple', 'geometric', 'medial', 'weighted']
        self._nbr_periods = [3, 5, 7, 0]

        # hdr = list(self._triangle.columns.values)
        # indx = list(self._triangle.index.values)
        #
        # for i in range(len(indx)):
        #     iteridx = indx[i]
        #     lastidx = len(indx)-1-i
        #
        #     for j in range(len(hdr)):
        #         iterhdr = hdr[j]
        #         if j==0:
        #             if np.isnan(self._triangle.iloc[i, j]):
        #                 self._triangle.set_value(iteridx, iterhdr, 1.)
        #
        #         elif self._triangle.iloc[i, j] < 1:
        #             self._triangle.set_value(iteridx, iterhdr, 1.)
        #
        #         if j > lastidx:
        #             self._triangle.set_value(iteridx, iterhdr, np.nan)
        self._triangle = self._triangle.cumsum(axis=1)





    @property
    def a2a(self):
        """Return pandas DataFrame of age-to-age factors based on triangle.
           will have 1 less row and 1 less column than the Cumulative
           triangle.
        """
        if self._a2a is None:

            hdr = list(self._triangle.columns)
            indx = list(self._triangle.index)
            self._a2a = self._triangle.applymap(lambda x: np.nan)

            for i in range(len(hdr) - 1):
                a2ahdr = str(hdr[i]) + "-" + str(hdr[i + 1])
                self._a2a.rename(columns={hdr[i]: a2ahdr}, inplace=True)

            # drop last column and last row =>
            drop_col = self._a2a.columns[-1]
            self._a2a.drop(drop_col, axis=1, inplace=True)

            # drop last row =>
            drop_row = self._a2a.index[-1]
            self._a2a.drop(drop_row, axis=0, inplace=True)

            # populate a2a with values from _triangle =>
            trihdr = list(self._triangle.columns.values)
            triindx = list(self._triangle.index.values)
            a2ahdr = list(self._a2a.columns.values)
            a2aindx = list(self._a2a.index.values)

            for i in range(len(a2aindx)):

                a2aindxval = a2aindx[i]

                for j in range(len(a2ahdr)):

                    a2ahdrval = a2ahdr[j]
                    itertri_1 = self._triangle.iloc[i,j]
                    itertri_2 = self._triangle.iloc[i,j+1]

                    if np.isnan(itertri_1) or itertri_1 < 1:
                        itera2a = np.nan

                    elif np.isnan(itertri_2) or itertri_2 < 1:
                        itera2a = np.nan

                    else:
                        itera2a = (itertri_2/itertri_1)

                    self._a2a.set_value(a2aindxval, a2ahdrval, itera2a)

        return (self._a2a)


    @staticmethod
    def _geometric(vals, weights=None):
        """
        Return the geometric average of the elements of vals.
        """
        if len(vals)==0:
            return(None)
        else:
            vals = list(vals)
            return(np.prod(vals)**(1/len(vals)))


    @staticmethod
    def _simple(vals, weights=None):
        """
        Return the simple average of elements of vals.
        """
        if len(vals)==0:
            return(None)
        else:
            return(sum(i for i in vals)/len(vals))


    @staticmethod
    def _medial(vals, weights=None):
        """
        Return the medial average of elements in vals. Medial
        average eliminates the min and max values, then returns
        the arithmetic average of the remaining items.
        """
        vals = list(vals)
        if   len(vals)==0: avg = None
        if   len(vals)==1: avg = vals[0]
        elif len(vals)==2: avg = sum(vals)/len(vals)
        else:
            max_indx = vals.index(max(vals))
            vals.remove(vals[max_indx])
            min_indx = vals.index(min(vals))
            vals.remove(vals[min_indx])
            avg = sum(vals)/len(vals)
        return(avg)



    def a2a_avgs(self, addl_avgs=None, func=None, **kwargs):
        """
        Return a DataFrame of various age-to-age factor averages.
        **kwargs can contain a user-defined function that computes
        a non-standard average for age-to-age factors. Set 'func' to
        the average computing function, that takes 1 argument, namely
        the column of values that will be averaged by each average
        duration present in self._nbr_periods.
        """
        #pd.options.display.float_format = '{:.5f}'.format

        dfc = self._triangle
        dfa = self.a2a
        ncols = self.a2a.shape[1]
        nrows = self.a2a.shape[0]

        # create lookup table for various average functions =>
        avgfuncs = {
            'simple'   :self._simple,
            'geometric':self._geometric,
            'medial'   :self._medial,
            'weighted' :None
            }


        indxstrs = list()
        iternbrprds = [i for i in self._nbr_periods]

        # add additional average durations =>
        if addl_avgs is not None:
            if isinstance(addl_avgs, list):
                for i in addl_avgs:
                    if isinstance(i, (int, float)):
                        if i not in iternbrprds:
                            if i <= nrows:
                                iternbrprds.append(i)
            else:
                if isinstance(i, (int, float)):
                    if addl_avgs not in iternbrprds:
                        if addl_avgs <= nrows:
                            iternbrprds.append(addl_avgs)

        # place `0` entry to last element in list =>
        iternbrprds = sorted(iternbrprds)
        iternbrprds.remove(0)
        iternbrprds.append(0)


        a2a_avg_lst = list(
                    itertools.product(self._avg_types, iternbrprds)
                    )

        for i in a2a_avg_lst:

            iteravg = i[0]
            iterdur = i[1]

            if iterdur==0:
                iterstr = "all-" + str(iteravg)
            else:
                iterstr = str(iterdur) + "-" + str(iteravg)
            indxstrs.append(iterstr)

        indx = sorted(a2a_avg_lst, key=lambda x: x[1])
        a2ahdrs = dfa.columns.values
        avgsdf = pd.DataFrame(index=indxstrs, columns=a2ahdrs)

        for a in enumerate(a2a_avg_lst):

            duration = a[1][1]
            avgtype = a[1][0]
            indxpos = a[0]
            indxstr = indxstrs[indxpos]
            iterfunc = avgfuncs[avgtype]

            for col in range(ncols):

                itercol = dfa.iloc[:, col]
                colpos = col
                colstr = a2ahdrs[col]
                iterstr = str(avgtype) + "-" + \
                          str(duration) + "-" + \
                          str(col) + "-" + \
                          indxstr + "-" + \
                          colstr

                if avgtype=='weighted':

                    t_ic_1 = dfc.iloc[:, col]
                    t_ic_2 = dfc.iloc[:, (col + 1)]

                    # find first NaN value in t_ic_2 =>
                    first_nan_year = t_ic_2.index[t_ic_2.apply(np.isnan)][0]
                    first_nan_indx = t_ic_2.index.searchsorted(first_nan_year)
                    final_cell_indx = first_nan_indx

                    if duration==0: first_cell_indx = 0

                    else:
                        first_cell_indx = (final_cell_indx - duration) if \
                                              (final_cell_indx - duration) >= 0 else 0

                    # divide sum of t_ic_2 by t_ic_1 =>
                    ic_2 = t_ic_2[first_cell_indx:final_cell_indx]
                    ic_1 = t_ic_1[first_cell_indx:final_cell_indx]
                    sum_ic_2 = t_ic_2[first_cell_indx:final_cell_indx].sum()
                    sum_ic_1 = t_ic_1[first_cell_indx:final_cell_indx].sum()
                    iteravg = (sum_ic_2/sum_ic_1)

                else: # avgtype in ('simple', 'geometric', 'medial')

                    # find index of first row with NaN =>
                    if any(itercol.map(lambda x: np.isnan(x))):

                        first_nan_year  = itercol.index[itercol.apply(np.isnan)][0]
                        first_nan_indx  = itercol.index.searchsorted(first_nan_year)
                        final_cell_indx = first_nan_indx

                        if duration==0:
                            first_cell_indx = 0

                        else:
                            first_cell_indx = (final_cell_indx - duration) if \
                                (final_cell_indx - duration) >= 0 else 0

                    else:
                        # when itercol has 0 NaN's
                        final_cell_indx = len(itercol)
                        first_cell_indx = 0 if duration==0 else (final_cell_indx-duration)

                    iteravg = iterfunc(itercol[first_cell_indx:final_cell_indx])
                    iterstr+="-"+str(iteravg)

                # write iteravg to avgdf =>
                avgsdf.loc[indxstr][colstr] = iteravg

        return(avgsdf)














# =============================================================================
# Unified Implementation
# =============================================================================


class Triangle:

    def __init__(self, data, origin=None, dev=None, value=None):
        """
        Transform data into a loss development triangle. `data` can be
        either a path to a delimited file or a pandas DataFrame.
        """











"""Transform a dataset into a loss triangle."""
if isinstance(data, pd.DataFrame):
    dataset = data
elif os.path.isfile(data):  # read delimited file into DataFrame
    if sep is None:  # use csv module to identify delimiter
        with open(data, "r") as f:
            hdr = next(f).replace(" ", "")
            snfr = csv.Sniffer()
            dialect = snfr.sniff(hdr)
            sep = dialect.delimiter

    dataset = pd.read_table(data, sep=sep)

# keep only necessary fields, and aggregate by origin & dev =>
dataset = dataset[[origin, dev, value]]
dataset = dataset.groupby([origin, dev], as_index=False).sum()

# transform dataset into incremental loss triangle =>
tri = dataset.pivot(index=origin, columns=dev).rename_axis(None)
tri.columns = tri.columns.droplevel(0)

pd.DataFrame.__init__(self, tri)
self._triangle = tri
self._iscumulative = None
self._latest_diagonal = None
self._dev_periods = None
self._origin_yrs = None
self.tri_field = None
self.tri_desc = None
self.tritype = None
self.origin = origin
self.value = value
self.data = data
self.dev = dev
self.sep = sep
# self.inc = inc


def __init__(self, data, sep=None, origin=None, dev=None,
         value=None):
BaseTriangle.__init__(self, data, sep, origin, dev, value)
hdr = list(self._triangle.columns.values)
indx = list(self._triangle.index.values)

for i in range(len(indx)):

    iteridx = indx[i]
    lastidx = len(indx) - 1 - i

    for j in range(len(hdr)):

        iterhdr = hdr[j]

        if j <= lastidx:

            if self._triangle.iloc[i, j] < 1:
                self._triangle.set_value(iteridx, iterhdr, 1.)



















