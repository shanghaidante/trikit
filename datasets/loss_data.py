import sys
sys.path.append("U:\\Repos")
import numpy as np
import pandas as pd
import pickle
import os.path
import trikit


_incrd = os.path.split(trikit.__file__)[0] + "\\datasets\\incrd.pkl"
_bulk = os.path.split(trikit.__file__)[0] + "\\datasets\\bulk.pkl"
_paid = os.path.split(trikit.__file__)[0] + "\\datasets\\paid.pkl"

lobs = ['workers_comp', 'prod_liab', 'pp_auto', 'other_liab', 'med_mal', 'com_auto']

# using filter dataframe to relevant groups ===================================================>
# df = pd.read_table("U:\\Repos\\trikit\\Sample_Data\\CAS_Loss_Data_Agg.csv", sep=",")
# df.rename(
#     columns={'ACCIDENT_YEAR':'ORIGIN','DEVELOPMENT_PERIOD':'DEV_PERIOD'},
#     inplace=True
#     )
#
#
# workers_comp_paid = df.query("LOSS_TYPE=='WC'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
# prod_liab_paid    = df.query("LOSS_TYPE=='PROD_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
# pp_auto_paid      = df.query("LOSS_TYPE=='PP_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
# other_liab_paid   = df.query("LOSS_TYPE=='OTHR_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
# med_mal_paid      = df.query("LOSS_TYPE=='MED_MAL'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
# com_auto_paid     = df.query("LOSS_TYPE=='COM_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'CUM_PAID_LOSS']]
#
# workers_comp_incrd = df.query("LOSS_TYPE=='WC'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
# prod_liab_incrd    = df.query("LOSS_TYPE=='PROD_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
# pp_auto_incrd      = df.query("LOSS_TYPE=='PP_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
# other_liab_incrd   = df.query("LOSS_TYPE=='OTHR_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
# med_mal_incrd      = df.query("LOSS_TYPE=='MED_MAL'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
# com_auto_incrd     = df.query("LOSS_TYPE=='COM_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'INCRD_LOSS']]
#
# workers_comp_bulk = df.query("LOSS_TYPE=='WC'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
# prod_liab_bulk    = df.query("LOSS_TYPE=='PROD_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
# pp_auto_bulk      = df.query("LOSS_TYPE=='PP_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
# other_liab_bulk   = df.query("LOSS_TYPE=='OTHR_LIAB'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
# med_mal_bulk      = df.query("LOSS_TYPE=='MED_MAL'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
# com_auto_bulk     = df.query("LOSS_TYPE=='COM_AUTO'")[['ORIGIN', 'DEV_PERIOD', 'BULK_LOSS']]
#
#
# incrd_kv ={
#     'workers_comp':workers_comp_incrd,
#     'prod_liab'   :prod_liab_incrd,
#     'pp_auto'     :pp_auto_incrd,
#     'other_liab'  :other_liab_incrd,
#     'med_mal'     :med_mal_incrd,
#     'com_auto'    :com_auto_incrd
#     }
# paid_kv ={
#     'workers_comp':workers_comp_paid,
#     'prod_liab'   :prod_liab_paid,
#     'pp_auto'     :pp_auto_paid,
#     'other_liab'  :other_liab_paid,
#     'med_mal'     :med_mal_paid,
#     'com_auto'    :com_auto_paid
#     }
# bulk_kv ={
#     'workers_comp':workers_comp_bulk,
#     'prod_liab'   :prod_liab_bulk,
#     'pp_auto'     :pp_auto_bulk,
#     'other_liab'  :other_liab_bulk,
#     'med_mal'     :med_mal_bulk,
#     'com_auto'    :com_auto_bulk
#     }
#
#
# with open(_incrd, "wb") as fincrd:
#     pickle.dump(incrd_kv, fincrd, pickle.HIGHEST_PROTOCOL)
#
# with open(_bulk, "wb") as fbulk:
#     pickle.dump(bulk_kv, fbulk, pickle.HIGHEST_PROTOCOL)
#
# with open(_paid, "wb") as fpaid:
#     pickle.dump(paid_kv, fpaid, pickle.HIGHEST_PROTOCOL)



# read in datasets ===========================================================>
# with open(_incrd, 'rb') as fincrd:
#     incrd_kv = pickle.load(fincrd)
#     workers_comp = incrd_kv['workers_comp']
#     prod_liab    = incrd_kv['prod_liab']
#     pp_auto      = incrd_kv['pp_auto']
#     other_liab   = incrd_kv['other_liab']
#     med_mal      = incrd_kv['med_mal']
#     com_auto     = incrd_kv['com_auto']


# with open(_incrd, 'rb') as fincrd:
#     incrd_kv = pickle.load(fincrd)
#     workers_comp_incrd = incrd_kv['workers_comp']
#     prod_liab_incrd    = incrd_kv['prod_liab']
#     pp_auto_incrd      = incrd_kv['pp_auto']
#     other_liab_incrd   = incrd_kv['other_liab']
#     med_mal_incrd      = incrd_kv['med_mal']
#     com_auto_incrd     = incrd_kv['com_auto']
#
#
# with open(_paid, 'rb') as fpaid:
#     paid_kv = pickle.load(fpaid)
#     workers_comp_paid = paid_kv['workers_comp']
#     prod_liab_paid    = paid_kv['prod_liab']
#     pp_auto_paid      = paid_kv['pp_auto']
#     other_liab_paid   = paid_kv['other_liab']
#     med_mal_paid      = paid_kv['med_mal']
#     com_auto_paid     = paid_kv['com_auto']
#
#
# with open(_bulk, 'rb') as fbulk:
#     bulk_kv = pickle.load(fbulk)
#     workers_comp_bulk = bulk_kv['workers_comp']
#     prod_liab_bulk    = bulk_kv['prod_liab']
#     pp_auto_bulk      = bulk_kv['pp_auto']
#     other_liab_bulk   = bulk_kv['other_liab']
#     med_mal_bulk      = bulk_kv['med_mal']
#     com_auto_bulk     = bulk_kv['com_auto']




def load(lob="workers_comp"):
    """
    Load and return the incurred loss dataset for the specified
    line of business (lob). By default, returns workers
    compensation incurred loss data. In addition to workers
    compenstaion loss data, lob can be set to any of:

        'prod_liab'  => Products Liability incurred loss data
        'pp_auto'    => Personal Auto incurred loss data
        'other_liab' => Other Liability incurred loss data
        'med_mal'    => Medical Malpractice incurred loss data
        'com_auto'   => Commercial Auto incurred loss data

    For all lob's, the dataset is returned as a 3-field pandas
    DataFrame with fields `ORIGIN`, `DEV_PERIOD` and `INCRD_LOSS`.
    """
    fpath = os.path.split(trikit.__file__)[0] + "\\datasets\\incrd.pkl"

    with open(fpath, 'rb') as f:
        incrd_kv = pickle.load(f)
        workers_comp = incrd_kv['workers_comp']
        prod_liab = incrd_kv['prod_liab']
        pp_auto = incrd_kv['pp_auto']
        other_liab = incrd_kv['other_liab']
        med_mal = incrd_kv['med_mal']
        com_auto = incrd_kv['com_auto']

    if   lob=="workers_comp": data = workers_comp
    elif lob=="prod_liab": data = prod_liab
    elif lob=="pp_auto": data = pp_auto
    elif lob=="other_liab": data = other_liab
    elif lob=="med_mal": data = med_mal
    elif lob=="com_auto": data = com_auto
    else:
        raise KeyError("{} is not a valid key.".format(lob))
    return(data)












