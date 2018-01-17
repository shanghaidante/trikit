import sys; sys.path.append("E:\\Repos\\")
import unittest
import trikit
import pandas as pd
import numpy as np
import os
import os.path
import decimal
import logging

from trikit.triangle import _BaseTriangle, _IncrTriangle, _CumTriangle, _Triangle




# TESTING_STATE can be either "print" or "log" =>
TESTING_STATE = "print"



ff0 = "E:\\Repos\\trikit\\datasets\\RAA.csv"
ds0 = pd.read_csv(ff0)

ff1 = "E:\\Repos\\trikit\\datasets\\WestBendMutual.csv"
ds1 = pd.read_csv(ff1); ds1 = ds1[ds1["LOSS_KEY"]=="WC"]

t1 = _Triangle(ds0, origin='ORIGIN',dev='DEV',value='VALUE')
t2 = _Triangle(ds1, origin='ORIGIN',dev='DEV_PERIOD',value='INCRD_LOSS')

i1 = t1.incr
i2 =  _IncrTriangle(trisize=10)
i3 = _IncrTriangle()


c1 = t1.cum
c2 = _CumTriangle(trisize=10, incr=False)
c3 = _CumTriangle(incr=False)


# Convert incremental triangle to cumulative.
i2c = _CumTriangle(i1)


# Convert cumulative triangle to incremental.
c2i = _IncrTriangle(c1)
ctri = _Triangle(ds0, origin='ORIGIN',dev='DEV',value='VALUE').cumulative



ta = trikit.load("ta83")

sf = trikit.load("sf")
sf1 = trikit.load("sf",lob="com_auto")




# ChainLadder tests =>
# cl = trikit.ChainLadder(ds0,origin='ORIGIN',dev='DEV',value='VALUE', tail_fact=1.05)
#
# # Get age to ultimate factors
# cl.age2ult
#
# cl.squared_tri


mcl = trikit.MackChainLadder(ta,origin='ORIGIN',dev='DEV',value='VALUE', tail_fact=1.)
mcl.mack_stderr









# Test Suite => Print or log diagnostics =====================================>
if TESTING_STATE=="print:

    # _IncrTriangle Tests =>
    print("<>=<>=<>=<> `_IncrTriangle` => i1 [Actual Data] <>=<>=<>=<>")
    print("i1.latest_diag     : {}".format(i1.latest_diag))
    print("i1.dev_periods     : {}".format(i1.dev_periods))
    print("i1.origin_yrs      : {}".format(i1.origin_yrs))
    print("i1.get_origin(1989): {}".format(i1.get_origin(1989)))
    print("i1.get_dev(4)      : {}".format(i1.get_dev(4)))
    print("")
    
    print("<>=<>=<>=<> `_IncrTriangle` => i2 [All NaNs]    <>=<>=<>=<>")
    print("i2.latest_diag     : {}".format(i2.latest_diag))
    print("i2.dev_periods     : {}".format(i2.dev_periods))
    print("i2.origin_yrs      : {}".format(i2.origin_yrs))
    print("i2.get_origin(1989): {}".format(i2.get_origin(1989)))
    print("i2.get_dev(4)      : {}".format(i2.get_dev(4)))
    print("")
    
    print("<>=<>=<>=<> `_IncrTriangle` => i3 [0-rows/cols] <>=<>=<>=<>")
    print("i3.latest_diag     : {}".format(i3.latest_diag))
    print("i3.dev_periods     : {}".format(i3.dev_periods))
    print("i3.origin_yrs      : {}".format(i3.origin_yrs))
    print("i3.get_origin(1989): {}".format(i3.get_origin(1989)))
    print("i3.get_dev(4)      : {}".format(i3.get_dev(4)))
    print("")
    

    # _CumTriangle Tests =>
    print("<>=<>=<>=<> `_CumTriangle` - c1 - [Actual Data] <>=<>=<>=<>")
    print("c1.latest_diag              : {}".format(c1.latest_diag))
    print("c1.dev_periods              : {}".format(c1.dev_periods))
    print("c1.origin_yrs               : {}".format(c1.origin_yrs))
    print("c1.get_origin(1989)         : {}".format(c1.get_origin(1989)))
    print("c1.get_dev(4)               : {}".format(c1.get_dev(4)))
    print("c1.a2a                      : {}".format(c1.a2a))
    print("c1.a2a_avgs()               :\n{}\n".format(c1.a2a_avgs()))
    print("c1.a2a_avgs(addl_avgs=8)    :\n{}\n".format(c1.a2a_avgs(addl_avgs=8)))
    print("c1.a2a_avgs(addl_avgs=[6,8]):\n{}\n".format(c1.a2a_avgs(addl_avgs=[6,8])))
    print("")
    
    print("<>=<>=<>=<> `_CumTriangle` - c2 - [All NaNs]    <>=<>=<>=<>")
    print("c2.latest_diag              : {}".format(c2.latest_diag))
    print("c2.dev_periods              : {}".format(c2.dev_periods))
    print("c2.origin_yrs               : {}".format(c2.origin_yrs))
    print("c2.get_origin(1989)         : {}".format(c2.get_origin(1989)))
    print("c2.get_dev(4)               : {}".format(c2.get_dev(4)))
    print("c2.a2a                      : {}".format(c2.a2a))
    print("c2.a2a_avgs()               :\n{}\n".format(c2.a2a_avgs()))
    print("c2.a2a_avgs(addl_avgs=6)    :\n{}\n".format(c2.a2a_avgs(addl_avgs=6)))
    print("c2.a2a_avgs(addl_avgs=[4,9]):\n{}\n".format(c2.a2a_avgs(addl_avgs=[4,9])))
    print("")
    
    print("<>=<>=<>=<> `_CumTriangle` - c3 - [0-rows/cols] <>=<>=<>=<>")
    print("c3.latest_diag              : {}".format(c3.latest_diag))
    print("c3.dev_periods              : {}".format(c3.dev_periods))
    print("c3.origin_yrs               : {}".format(c3.origin_yrs))
    print("c3.get_origin(1989)         : {}".format(c3.get_origin(1989)))
    print("c3.get_dev(4)               : {}".format(c3.get_dev(4)))
    print("c3.a2a                      : {}".format(c3.a2a))
    print("c3.a2a_avgs()               :\n{}\n".format(c3.a2a_avgs()))
    print("c3.a2a_avgs(addl_avgs=4)    :\n{}\n".format(c3.a2a_avgs(addl_avgs=4)))
    print("c3.a2a_avgs(addl_avgs=[6,4]):\n{}\n".format(c3.a2a_avgs(addl_avgs=[6,4])))
    print("")




elif TESTING)STATE=="log":

    logging.basicConfig(
            filename="U:/trikit/Logging/trikit_unittests.txt",
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
            )

    # _IncrTriangle Tests =>
    logging.debug("<>=<>=<>=<> `_IncrTriangle` => i1 [Actual Data] <>=<>=<>=<>")
    logging.debug("i1.latest_diag     : {}".format(i1.latest_diag))
    logging.debug("i1.dev_periods     : {}".format(i1.dev_periods))
    logging.debug("i1.origin_yrs      : {}".format(i1.origin_yrs))
    logging.debug("i1.get_origin(1989): {}".format(i1.get_origin(1989)))
    logging.debug("i1.get_dev(4)      : {}".format(i1.get_dev(4)))
    logging.debug("")

    logging.debug("<>=<>=<>=<> `_IncrTriangle` => i2 [All NaNs]    <>=<>=<>=<>")
    logging.debug("i2.latest_diag     : {}".format(i2.latest_diag))
    logging.debug("i2.dev_periods     : {}".format(i2.dev_periods))
    logging.debug("i2.origin_yrs      : {}".format(i2.origin_yrs))
    logging.debug("i2.get_origin(1989): {}".format(i2.get_origin(1989)))
    logging.debug("i2.get_dev(4)      : {}".format(i2.get_dev(4)))
    logging.debug("")

    logging.debug("<>=<>=<>=<> `_IncrTriangle` => i3 [0-rows/cols] <>=<>=<>=<>")
    logging.debug("i3.latest_diag     : {}".format(i3.latest_diag))
    logging.debug("i3.dev_periods     : {}".format(i3.dev_periods))
    logging.debug("i3.origin_yrs      : {}".format(i3.origin_yrs))
    logging.debug("i3.get_origin(1989): {}".format(i3.get_origin(1989)))
    logging.debug("i3.get_dev(4)      : {}".format(i3.get_dev(4)))
    logging.debug("")



    # _CumTriangle Tests =>
    logging.debug("<>=<>=<>=<> `_CumTriangle` - c1 - [Actual Data] <>=<>=<>=<>")
    logging.debug("c1.latest_diag              : {}".format(c1.latest_diag))
    logging.debug("c1.dev_periods              : {}".format(c1.dev_periods))
    logging.debug("c1.origin_yrs               : {}".format(c1.origin_yrs))
    logging.debug("c1.get_origin(1989)         : {}".format(c1.get_origin(1989)))
    logging.debug("c1.get_dev(4)               : {}".format(c1.get_dev(4)))
    logging.debug("c1.a2a                      : {}".format(c1.a2a))
    logging.debug("c1.a2a_avgs()               :\n{}\n".format(c1.a2a_avgs()))
    logging.debug("c1.a2a_avgs(addl_avgs=8)    :\n{}\n".format(c1.a2a_avgs(addl_avgs=8)))
    logging.debug("c1.a2a_avgs(addl_avgs=[6,8]):\n{}\n".format(c1.a2a_avgs(addl_avgs=[6,8])))
    logging.debug("")

    logging.debug("<>=<>=<>=<> `_CumTriangle` - c2 - [All NaNs]    <>=<>=<>=<>")
    logging.debug("c2.latest_diag              : {}".format(c2.latest_diag))
    logging.debug("c2.dev_periods              : {}".format(c2.dev_periods))
    logging.debug("c2.origin_yrs               : {}".format(c2.origin_yrs))
    logging.debug("c2.get_origin(1989)         : {}".format(c2.get_origin(1989)))
    logging.debug("c2.get_dev(4)               : {}".format(c2.get_dev(4)))
    logging.debug("c2.a2a                      : {}".format(c2.a2a))
    logging.debug("c2.a2a_avgs()               :\n{}\n".format(c2.a2a_avgs()))
    logging.debug("c2.a2a_avgs(addl_avgs=6)    :\n{}\n".format(c2.a2a_avgs(addl_avgs=6)))
    logging.debug("c2.a2a_avgs(addl_avgs=[4,9]):\n{}\n".format(c2.a2a_avgs(addl_avgs=[4,9])))
    logging.debug("")

    logging.debug("<>=<>=<>=<> `_CumTriangle` - c3 - [0-rows/cols] <>=<>=<>=<>")
    logging.debug("c3.latest_diag              : {}".format(c3.latest_diag))
    logging.debug("c3.dev_periods              : {}".format(c3.dev_periods))
    logging.debug("c3.origin_yrs               : {}".format(c3.origin_yrs))
    logging.debug("c3.get_origin(1989)         : {}".format(c3.get_origin(1989)))
    logging.debug("c3.get_dev(4)               : {}".format(c3.get_dev(4)))
    logging.debug("c3.a2a                      : {}".format(c3.a2a))
    logging.debug("c3.a2a_avgs()               :\n{}\n".format(c3.a2a_avgs()))
    logging.debug("c3.a2a_avgs(addl_avgs=4)    :\n{}\n".format(c3.a2a_avgs(addl_avgs=4)))
    logging.debug("c3.a2a_avgs(addl_avgs=[6,4]):\n{}\n".format(c3.a2a_avgs(addl_avgs=[6,4])))
    logging.debug("")





# ti0 = _IncrTriangle(ds0, origin='ORIGIN', dev='DEV', value='VALUE')
# tc0 = _CumTriangle(ds0,  origin='ORIGIN', dev='DEV', value='VALUE')
# ti1 = _IncrTriangle(ds1,origin='ORIGIN',dev='DEV_PERIOD',value='INCRD_LOSS')
# tc1 = _CumTriangle(ds1,origin='ORIGIN', dev='DEV_PERIOD',value='INCRD_LOSS')