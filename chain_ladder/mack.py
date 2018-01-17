from ..chain_ladder import ChainLadder
import numpy as np
import pandas as pd



class MackChainLadder(ChainLadder):
    """
    Perform Mack Chain Ladder method.
    """
    def __init__(self, data, **kwargs):

        super().__init__(data, **kwargs)

        # properties
        self._mack_stderr = None



    @property
    def mack_stderr(self):
        """
        Return the square of the standard error for each of the n-1
        development periods as numpy array.
        """
        if self._mack_stderr is None:

            n = self.tri.columns.size
            self._mack_stderr = np.zeros(n-1, dtype=np.float_)

            for k in range(n-2):
                iter_ses = 0  # `square of standard error`

                for i in range(n-(k+1)):
                    c_1, c_2 = self.tri.iloc[i,k], self.tri.iloc[i,k+1]
                    iter_ses+=c_1*((c_2/c_1)-self.selarr[k])**2

                iter_ses = iter_ses/(n-k-2)
                self._mack_stderr[k] = iter_ses

            try:
                # Calculate standard error for dev period n-1.
                self._mack_stderr[-1] = \
                    np.min((
                        self._mack_stderr[-2]**2/self._mack_stderr[-3],
                        np.min([self._mack_stderr[-2],self._mack_stderr[-3]])
                        ))

            except ZeroDivisionError: self._mack_stderr[-1] = 0

        return(self._mack_stderr)





# @property
#     def mack_stderr(self):
#         """
#         Return an array containing the square of the standard error
#         for each of the n-1 development periods.
#         """
#         if self._mack_stderr is None:
#
#             self._mack_stderr = list()
#
#             n = self.tri.columns.size
#
#             for k in range(n-2):
#
#                 col_k = k + 1
#                 #f_k =
#                 #iter_mult = 1/(n-col_k-1)
#                 iter_var = 0
#
#                 for i in range(n-col_k):
#                     c_1, c_2 = self.tri.iloc[i, k], self.tri.iloc[i, k+1]
#                     iter_var+=c_1*((c_2/c_1)-self.selarr[k])**2
#
#                 iter_var = iter_var/(n-col_k-1)
#                 self._mack_stderr.append(iter_var)
#
#         return(np.array(self._mack_stderr, dtype=np.float_))














