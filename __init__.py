"""
<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>
|  _                                                                     |
| | |_ _ __(_) | _(_) |_                                                 |
| | __| '__| | |/ / | __|                                                |
| | |_| |  | |   <| | |_                                                 |
|  \__|_|  |_|_|\_\_|\__|                                                |
|_______________________________________________________________________ |
|                                                                        |
| Actuarial Reserving Methods in Python                                  |
| Created by      => James D Triveri <<<james.triveri@gmail.com>>>       |
| License         => 3-Clause BSD                                        |
| Repository Link => https://github.com/jtrive84/trikit                  |
|                                                                        |
<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>=<>

Outstanding Tasks =>

 1.] Implement option to generate random incremental loss data

 2.] Ability to write triangle to file as .xlsx (using win32)

 3.] Add ability to add user-defined functions to a2a_avgs

 4.] Find out how to suppress scientific notation without distorting the
     appearance of NaN's in DataFrames

 5.] Implement option to output loss emergence as panneled exhibit

 6.] Fix datasets

 7.]

 8.]

 9.]

10.]

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

To compute percentiles:

    np.percentile(a, 100*y, axis=None)

    # set axis to 1 if computing percentile on column from a2a triangle

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

# Unit tests should be added (if possible) for each added feature.
# Adding more unit tests should be done by creating a new test module,
# adding a suite() method which returns a TestSuite object with all
# the testcases in it.
import pandas as pd
import numpy as np
import scipy
import os
import sys
import collections
import datetime
import os.path
from .triangle import _BaseTriangle, _IncrTriangle, _CumTriangle, _Triangle
# from .datasets import loss_data
#from .methods import chain_ladder, bootstrap
from .utils import *

#from .utils import LOBS


# extend PYTHONPATH `trikit` base directory
#sys.path.extend([
# print(os.path.realpath(__file__))


# make available at top-level of trikit
# ChainLadder = chain_ladder.ChainLadder
# Bootstrap = bootstrap.Bootstrap



# make sample datasets available at trikit top-level
#load = loss_data.load



pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 500)

np.set_printoptions(
            edgeitems=3,
            linewidth=200,
            suppress=True,
            nanstr='NaN',
            infstr='Inf',
            precision=5
            )


# pd.set_option('display.chop_threshold', 1.00)
# pd.options.display.float_format = '{:.0f}'.format
# pd.options.display.float_format = '{:12.0f}'.format

#np.set_printoptions(precision=0)
#pd.options.display.float_format = '{:.2f}'.format
#pd.set_option('display.precision', 0)
#pd.options.display.float_format = '{:.0f}'.format
#pd.options.display.float_format = '{:10.0f}'.format


# pd.set_option('precision', 0)

# np.set_printoptions(suppress=True)
# pd.options.display.float_format = '{:.0f}'.format
# pd.set_option('display.float_format', lambda x: '%.0f' % x)
# pd.options.display.float_format = '{:.2f}'.format
# pd.options.display.float_format = '{:10.0f}'.format

# curr_yr = datetime.datetime.today().strftime('%Y')
# results = collections.OrderedDict()
# accident_years = 10
# init_accident_year = int(curr_yr)-accident_years
# index = list(range(init_accident_year, int(curr_yr)))
#
# for i in range(accident_years):
#     iterarr = np.random.lognormal(10, .5, accident_years-i).tolist()
#     iterarr.extend([np.NaN]*i)
#     results[i] = iterarr
# rinc = pd.DataFrame(data=results, index=index)
# decimals = pd.Series([0]*10, index=range(10))
# rinc.round(decimals)
# print(type(rinc))
