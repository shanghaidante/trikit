"""
trikit Loss Reserving Methods
"""
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from trikit.triangle import (
    _BaseTriangle,
    _IncrTriangle,
    _CumTriangle,
    _Triangle
    )



class ChainLadder:
    """
    From the Casualty Actuarial Society's "Estimating Unpaid Claims Using
    Basic Techniques" Version 3 (Friedland, Jacqueline - 2010), the
    development method ('Chain Ladder') consists of seven basic steps:

        Step 1: Compile claims data in a development triangle
        Step 2: Calculate age-to-age factors
        Step 3: Calculate averages of the age-to-age factors
        Step 4: Select claim development factors
        Step 5: Select tail factor
        Step 6: Calculate cumulative claims
        Step 7: Project ultimate claims

    The ChainLadder constructor takes for input the specified age-2-age
    average (`sel`), along with a tail factor (`tail_fact`), and populates
    the the bottom-right section of the triangle.

    `data` can be either an instance of the _Triangle, _InrTriangle or
    _CumTriangle classes, or a DataFrame with `origin`, `dev` and
    `value` specified. If the field identifiers are not explicitly
    provided, the Triangle class constrcutors will check for literal
    fieldnames 'ORIGIN', 'DEV' and 'VALUE', but if not found, an
    exception will be raised.

    `sel` determines which set of age-to-age averages to use for
    calculating age-to-ultimate factors. If not specified, `sel`
    defaults to a weighted average over all accident years.

    `tail` represents the chain ladder tail factor (more detail here).
    By default, `tail` is set to 1.0.
    https://www.casact.org/pubs/forum/13fforum/02-Tail-Factors-Working-Party.pdf

    """
    def __init__(self, data, **kwargs):

        origin    = kwargs.get('origin', None)
        dev       = kwargs.get('dev', None)
        value     = kwargs.get('value', None)
        trisize   = kwargs.get('trisize', None)
        tail_fact = kwargs.get('tail_fact', 1.0)
        sel       = kwargs.get('sel', 'all-weighted')


        # Obtain cumulative triangle from specified data argument.
        if isinstance(data, _Triangle):
            self.tri = data.cumulative

        elif isinstance(data, _IncrTriangle):
            self.tri = _CumTriangle(data)

        elif isinstance(data, _CumTriangle):
            self.tri = data

        elif set(['origin','dev','value']).issubset(kwargs.keys()):
            self.tri = _Triangle(data,origin=origin,dev=dev,value=value).cum

        self.selstr = sel
        self.tail_fact = tail_fact
        self.selarr = self.tri.a2a_avgs.loc[self.selstr].values

        # properties
        self._squared_tri = None
        self._ultimates = None
        self._age2ult = None
        self._summary = None



    @property
    def age2ult(self):
        """
        Calculate the Age-to-Ultimate factors by successive multiplication
        beginning with the tail factor and the oldest age-to-age factor. The
        cumulative claim development factor projects the total growth over the
        remaining valuations. Cumulative claim development factors are also
        known as `Age-to-Ultimate Factors` or `Claim Development Factors to
        Ultimate`.
        """
        if self._age2ult is None:

            self._age2ult = \
                np.cumprod(np.append(self.selarr,self.tail_fact)[::-1])[::-1]

        return(self._age2ult.astype(np.float_))




    @property
    def squared_tri(self):
        """
        Project claims growth for each future development period. Returns a
        DataFrame of loss projections for each development period.
        """

        if self._squared_tri is None:

            self._squared_tri = self.tri.copy(deep=True)

            for j in range(self._squared_tri.shape[1]):

                if self._squared_tri.iloc[:,j].isnull().any():

                    for i in range(self._squared_tri.shape[0]):

                        if np.isnan(self._squared_tri.iloc[i, j]):

                            # Multiply cell to left of current by age-2-age factor.
                            cell2left = self._squared_tri.iloc[i,j-1]

                            self._squared_tri.iloc[i,j] = cell2left*self.selarr[j-1]

            # Append ultimates to self._full_tri.
            self._squared_tri = pd.merge(
                self._squared_tri,
                self.ultimates,
                right_index=True,
                left_index=True
                )

        return(self._squared_tri)




    @property
    def ultimates(self):
        """
        Ultimate claims are equal to the product of the latest valuation of
        claims (the amount show on the latest diagonal of cumulative claims
        triangle) and the appropriate Age-to-Ultimate factor. We determine
        the appropriate Age-to-Ultimate factor based on the age of each
        accident year, then multiply each accident year's claims at the
        latest valuation by its Age-to_ultimate factor.
        """
        if self._ultimates is None:

            self._ultimates = pd.DataFrame(
                                columns=['ultimate'], index=self.tri.index
                                )

            self._ultimates['ultimate'] = \
                    [i*j for i,j in  \
                         zip(self.tri.latest_diag, self.age2ult)][::-1]

        return(self._ultimates)



    @property
    def summary(self):
        """
        Return a DataFrame containing summary statistics resulting
        from applying the development method to tri. Resulting table
        will look like the following:

            [AY|MATURITY|REPORTED|AGE-TO-ULT|PROJECTED ULT]
        """
        if self._summary is None:

            summ_cols = ['LATEST','CLDF','ULTIMATE','RESERVE']

            self._summary = pd.DataFrame(
                                columns=summ_cols, index=self.tri.index
                                )

            # Populate self._summary with existing properties if available.
            self._summary['LATEST'] = self.tri.latest_diag[::-1]

            self._summary['CDF']    = self.age2ult[::-1]

            #print(self.age2ult[::-1])


            self._summary['ULTIMATE'] = self.ultimates

            # Append `Total` row to self._summary.
            #self._summary.loc['TOTAL'] = self._summary.sum(numeric_only=True)

            # Set CLDF Total value to `NaN`.
            #self._summary.loc['Total','CLDF'] = np.NaN

        return(self._summary)




df = pd.DataFrame({
    'LATEST':clr.tri.latest_diag,
    'AGE_TO_ULT':clr.age2ult,
    'ULTIMATE':clr.tri.latest_diag*clr.age2ult
    })

df[['ULTIMATE']]