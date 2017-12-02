"""
trikit Loss Reserving Methods
"""
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns


class BaseMethod:
    """
    Base class inherited by all loss reserving methods in trikit.
    """
    def __init__(self, triangle, selection='all-weighted', tail_factor=1.0):
        self.tail_factor = tail_factor
        self.selection = selection
        self.triangle = triangle



class ChainLadder:
    """
    From the Casualty Actuarial Society's "Estimating Unpaid Claims Using
    Basic Techniques" Version 3 (Friedland, Jacqueline - 2010), the
    development method ('Chain Ladder') consists of seven basic steps:

        * Step 1: Compile claims data in a development triangle
        * Step 2: Calculate age-to-age factors
        * Step 3: Calculate averages of the age-to-age factors
        * Step 4: Select claim development factors
        * Step 5: Select tail factor
        * Step 6: Calculate cumulative claims
        * Step 7: Project ultimate claims

    The ChainLadder constructor takes the specified age-2-age average,
    along with a tail factor, and squares the triangle.
    """
    def __init__(self, triangle, selection='all-weighted', tail_factor=1.0):
        #BaseTriangle.__init__(self, data, sep, origin, dev, value, cumulative=False)
        self.triangle = triangle
        self.selection = selection
        self.tail_factor = tail_factor
        self.a2a_avgs = self.triangle.a2a_avgs()
        self.selection_vals = self.a2a_avgs.loc[[selection,]]
        self.selection_vals['Ultimate'] = self.tail_factor
        self._squared_triangle = None
        self._ultimates = None
        self._age2ult = None



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
            return(
                np.cumprod(
                    self.selection_vals.iloc[0,][::-1])[::-1].to_frame().transpose()
                    )
        else:
            return(self._age2ult)




    @property
    def squared_triangle(self):
        """
        Project claims growth for each future development period. Returns a
        DataFrame of loss projections for each development period.
        """
        if self._squared_triangle is None:
            sqrdtri = self.triangle.copy(deep=True)
            tricols = sqrdtri.columns
            trirows = sqrdtri.index
            a2a = np.ravel(self.selection_vals.values)
            nrows, ncols = self.triangle.shape

            for colpos in range(ncols):

                if sqrdtri.iloc[:,colpos].isnull().any():

                    itera2a = a2a[colpos-1]

                    for rowpos in range(nrows):

                        iterval = sqrdtri.iloc[rowpos, colpos]

                        if np.isnan(iterval):
                            # get value at cell to immediate left =>
                            adjacent_cell = sqrdtri.iloc[rowpos, colpos - 1]
                            sqrdtri.iloc[rowpos, colpos] = adjacent_cell * itera2a

            # append ultimates to sqrdtri =>
            sqrdtri = pd.merge(sqrdtri, self.ultimates,
                                   right_index=True, left_index=True)

        else:
            sqrdtri = self._squared_triangle
        return(sqrdtri)




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
            ld = np.ravel(self.triangle.latest_diagonal.values)
            a2u = np.ravel(self.age2ult.values)
            trirows = self.triangle.index
            ultsdf = pd.DataFrame(columns=['ultimate'], index=trirows)
            ults = [i*j for i,j in zip(ld, a2u)][::-1]
            #ultsdf['Latest_Diagonal'] = ld[::-1]
            #ultsdf['Age_to_Ult'] = a2u[::-1]
            ultsdf['ultimate'] = ults
            #ultsdf = ultsdf[['Latest_Diagonal', 'Age_to_Ult', 'Ultimate']]
            #cl.ultimates.append(cl.ultimates.sum(numeric_only=True), ignore_index=True)
        else:
            ultsdf = self._ultimates
        return(ultsdf)



    def _summary(self):
        """
        Returns a DataFrame containing summary statistics resulting
        from applying the development method to triangle. Resulting table
        will look like the following:

        AY| AGE of AY@ Eval DATE| REPORTED| AGE-TO-ULT| PROJECTED ULT|
        """
        if self._summary is None:
            ld = np.ravel(self.triangle.latest_diagonal.values)
            a2u = np.ravel(self.age2ult.values)
            trirows = self.triangle.index
            ultsdf = pd.DataFrame(columns=['ultimate'], index=trirows)
            ults = [i * j for i, j in zip(ld, a2u)][::-1]
            ultsdf['Latest_Diagonal'] = ld[::-1]
            ultsdf['Age_to_Ult'] = a2u[::-1]
            ultsdf['Ultimate'] = ults
            ultsdf = ultsdf[['Latest_Diagonal', 'Age_to_Ult', 'Ultimate']]
            # cl.ultimates.append(cl.ultimates.sum(numeric_only=True), ignore_index=True)

        else:
            ultsdf = self._summary

        return (ultsdf)


