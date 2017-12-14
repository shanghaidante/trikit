import sys
sys.path.append("U:\\Repos\\")
import unittest
import trikit
import pandas as pd
import numpy as np
import os
import os.path
import decimal
import logging


logging.basicConfig(
        filename="U:/trikit_unittests.txt",
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )

# logging.debug('Entering a2a_avgs method')
# logging.debug(iterstr)
# logging.debug("Finished Processing")


# fmapping = {'origin'       :'LOSS_YR',
#             'dev'          :'DEV_PERIOD',
#             'paid_loss'    :'PAID_LOSS_NET_OF_SS_AND_DED',
#             'incurred_loss':'INCRED_LOSS_NET_OF_SS_DED',
#             'alae'         :'ALAE'}


# # RAA dataset ================================================================>
# raargs = {'origin':'ORIGIN','dev':'DEV', 'value':'VALUE'}
# fraa = "U:\\Repos\\trikit\\sample_data\\RAA.csv"
# dfraa = pd.read_table(fraa,  usecols=['ORIGIN', 'DEV', 'VALUE'], sep=',')
# traa = trikit._Incremental(dfraa, **raargs)
# t = trikit._Cumulative(dfraa, **raargs)
#
#
# # Small Business dataset =====================================================>
# incrdargs = {'origin':'LOSS_YR', 'dev':'DEV_PERIOD', 'value': 'INCRD'}
# paidargs  = {'origin':'LOSS_YR', 'dev':'DEV_PERIOD', 'value': 'PAID'}
# alaeargs  = {'origin':'LOSS_YR', 'dev':'DEV_PERIOD', 'value': 'ALAE'}
# ifargs    = {'origin':'LOSS_YR', 'dev':'DEV_PERIOD', 'value': 'INCRD_FREQ'}
# pfargs    = {'origin':'LOSS_YR', 'dev':'DEV_PERIOD', 'value': 'PAID_FREQ'}
#
# df = pd.read_csv("U:\\Repos\\trikit\\Sample_Data\\Small_Business_Claims.csv")
# df = df.query('LOSS_YR>2006')
#
# # incurred triangle ==========================================================>
# i = trikit._Incremental(df, **incrdargs)
# ic = trikit._Cumulative(df,  **incrdargs)
#
# # paid triangle ==============================================================>
# p = trikit._Incremental(df, **paidargs)
# pc = trikit._Cumulative(df, **paidargs)
#
# # alae triangle ==============================================================>
# a = trikit._Incremental(df, **alaeargs)
# ac = trikit._Cumulative(df, **alaeargs)
#
# # incurred frequency triangle ================================================>
# _if = trikit._Incremental(df, **ifargs)
# ifc  = trikit._Cumulative(df, **ifargs)
#
# # paid frequency triangle ====================================================>
# pf = trikit._Incremental(df, **pfargs)
# pfc = trikit._Cumulative(df, **pfargs)


# Test trikit functionality on builtin datasets ==============================>




##### Workers Compensation Data #####
# wc = trikit.load(lob="workers_comp")
# wci = trikit._Incremental(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# wcc = trikit._Cumulative(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")


### _Incremental =>
# print("wci.rowsum(1): {}".format(wci.rowsum(1988)))
# print("wci.rowsum(2): {}".format(wci.rowsum(1989)))
# print("wci.rowsum(3): {}".format(wci.rowsum(1990)))
# print("wci.rowsum(4): {}".format(wci.rowsum(4)))
# print("wci.rowsum(5): {}".format(wci.rowsum(5)))
# print("wci.colsum(1): {}".format(wci.colsum(1)))
# print("wci.colsum(2): {}".format(wci.colsum(2)))
# print("wci.colsum(3): {}".format(wci.colsum(3)))
# print("wci.colsum(4): {}".format(wci.colsum(4)))
# print("wci.colsum(5): {}".format(wci.colsum(5)))

# get_origin(self, origin_yr) =>
# print("wci.get_origin(1990): {}".format(wci.get_origin(1990)))
# print("wci.get_origin(1991): {}".format(wci.get_origin(1991)))
# print("wci.get_origin(1992): {}".format(wci.get_origin(1992)))
# print("wci.get_origin(1993): {}".format(wci.get_origin(1993)))
# print("wci.get_origin(1994): {}".format(wci.get_origin(1994)))
#
# # get_dev(self, dev_period) =>
# print("wci.get_dev(1): {}".format(wci.get_dev(1)))
# print("wci.get_dev(2): {}".format(wci.get_dev(2)))
# print("wci.get_dev(4): {}".format(wci.get_dev(4)))
# print("wci.get_dev(5): {}".format(wci.get_dev(5)))
#
# # save triangle to file =>
# wci.save_triangle("U:/wc_triangle.csv")
#
# # test dev periods =>
# print("workers_comp Dev Periods : {}".format(wci.dev_periods))
# print("workers_comp Origin Years: {}".format(wci.origin_yrs))
# print("workers_comp Latest Diag : {}".format(wci.latest_diagonal))
#
#
# ### _Cumulative =>
# # Test wcc.a2a functionality:
# print("workers_comp Age2Age Factors : \n\n{}".format(wcc.a2a))
# print("workers_comp Age2Age Averages: \n\n{}".format(wcc.a2a_avgs()))





# pp = trikit.load(lob="pp_auto")
# ppi = trikit._Incremental(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# ppc = trikit._Cumulative(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")


### _Incremental =>
# print("ppi.rowsum(1): {}".format(ppi.rowsum(1988)))
# print("ppi.rowsum(2): {}".format(ppi.rowsum(1989)))
# print("ppi.rowsum(3): {}".format(ppi.rowsum(1990)))
# print("ppi.rowsum(4): {}".format(ppi.rowsum(4)))
# print("ppi.rowsum(5): {}".format(ppi.rowsum(5)))
# print("ppi.colsum(1): {}".format(ppi.colsum(1)))
# print("ppi.colsum(2): {}".format(ppi.colsum(2)))
# print("ppi.colsum(3): {}".format(ppi.colsum(3)))
# print("ppi.colsum(4): {}".format(ppi.colsum(4)))
# print("ppi.colsum(5): {}".format(ppi.colsum(5)))

# get_origin(self, origin_yr) =>
# print("ppi.get_origin(1990): {}".format(ppi.get_origin(1990)))
# print("ppi.get_origin(1991): {}".format(ppi.get_origin(1991)))
# print("ppi.get_origin(1992): {}".format(ppi.get_origin(1992)))
# print("ppi.get_origin(1993): {}".format(ppi.get_origin(1993)))
# print("ppi.get_origin(1994): {}".format(ppi.get_origin(1994)))
#
# # get_dev(self, dev_period) =>
# print("ppi.get_dev(1): {}".format(ppi.get_dev(1)))
# print("ppi.get_dev(2): {}".format(ppi.get_dev(2)))
# print("ppi.get_dev(3): {}".format(ppi.get_dev(3)))
# print("ppi.get_dev(4): {}".format(ppi.get_dev(4)))
# print("ppi.get_dev(5): {}".format(ppi.get_dev(5)))
#
# # save triangle to file =>
# ppi.save_triangle("U:/wc_triangle.csv")
#
# # test dev periods =>
# print("pp_auto Dev Periods : \n{}".format(ppi.dev_periods))
# print("pp_auto Origin Years: \n{}".format(ppi.origin_yrs))
# print("pp_auto Latest Diag : \n{}".format(ppi.latest_diagonal))
#
#
# ### _Cumulative =>
# # Test ppc.a2a functionality:
# print("pp_auto Age2Age Factors : \n\n{}".format(ppc.a2a))
# print("pp_auto Age2Age Averages: \n\n{}".format(ppc.a2a_avgs()))




# pp = trikit.load(lob="pp_auto")
# ppi = trikit._Incremental(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# ppc = trikit._Cumulative(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
#
# wc = trikit.load(lob="workers_comp")
# wci = trikit._Incremental(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# wcc = trikit._Cumulative(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")

ff = "U:\\Repos\\trikit\\datasets\\RAA.csv"

raa = pd.read_csv(ff)


ppi = trikit._Incremental(ff, origin="ORIGIN", dev="DEV", value="VALUE")
ppc = trikit._Cumulative(ff, origin="ORIGIN", dev="DEV", value="VALUE")






cl = trikit.ChainLadder(ppc)
print(cl.ultimates)




# wc  = trikit.load(lob="workers_comp")
# wci = trikit._Incremental(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# wcc = trikit._Cumulative(wc, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
#
#
# pp  = trikit.load(lob="pp_auto")
# ppi = trikit._Incremental(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
# ppc = trikit._Cumulative(pp, origin="ORIGIN", dev="DEV_PERIOD", value="INCRD_LOSS")
#
#
# raa = pd.read_table("U:\\Repos\\trikit\\datasets\\RAA.csv", sep=",")
# rac = trikit._Cumulative(raa, origin='ORIGIN', dev='DEV', value='VALUE', iscum=True)
# racl = trikit.ChainLadder(rac, tail_factor=1.005)
#
# print(racl.squared_triangle)
# print("")
# print(racl.age2ult)



# chain ladder class =>
# wccl = trikit.ChainLadder(wcc)
# ppcl  = trikit.ChainLadder(ppc)


