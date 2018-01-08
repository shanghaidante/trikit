import sys; sys.path.append("U:\\Repos")
import numpy as np
import pandas as pd
import pickle
import os.path
import trikit
from collections import namedtuple




# Initialize namedtuple's for datasets with multiple LOB's.
WestBendMutual = namedtuple(
    'WestBendMutual',
        ['workers_comp', 'prod_liab', 'pp_auto', 'othr_liab', 'com_auto'],
        rename=True
        )
StateFarm = namedtuple(
        'StateFarm',
        ['workers_comp', 'prod_liab', 'pp_auto', 'othr_liab', 'com_auto'],
        rename=True
        )
Aegis = namedtuple(
        'Aegis',
        ['pp_auto', 'othr_liab', 'com_auto'],
        rename=True
        )


_wbm  = os.path.split(trikit.__file__)[0] + "\\datasets\\WestBendMutual.csv"
_sf   = os.path.split(trikit.__file__)[0] + "\\datasets\\StateFarm.csv"
_aeg  = os.path.split(trikit.__file__)[0] + "\\datasets\\Aegis.csv"
_raa  = os.path.split(trikit.__file__)[0] + "\\datasets\\RAA.csv"
_ta83 = os.path.split(trikit.__file__)[0] + "\\datasets\\TaylorAshe83.csv"
_lrdb = os.path.split(trikit.__file__)[0] + "\\datasets\\CAS_Loss_Reserve_Database.csv"


# wbm: ['WC', 'PROD_LIAB', 'PP_AUTO', 'OTHR_LIAB', 'COM_AUTO']
# sf : ['WC', 'PROD_LIAB', 'PP_AUTO', 'OTHR_LIAB', 'COM_AUTO']
# aeg: ['PP_AUTO', 'OTHR_LIAB', 'COM_AUTO']
wbm  = pd.read_csv(_wbm).reset_index().drop("index",axis=1)
sf   = pd.read_csv(_sf).reset_index().drop("index",axis=1)
aeg  = pd.read_csv(_aeg).reset_index().drop("index",axis=1)
raa  = pd.read_csv(_raa).reset_index().drop("index",axis=1)
ta83 = pd.read_csv(_ta83).reset_index().drop("index",axis=1)
lrdb = pd.read_csv(_lrdb).reset_index().drop("index",axis=1)


wbm.rename(columns={"DEV_PERIOD":"DEV"},inplace=True)
sf.rename(columns={"DEV_PERIOD":"DEV"},inplace=True)
aeg.rename(columns={"DEV_PERIOD":"DEV"},inplace=True)


# To access namedtuple fieldnames, use `wbm._fields`.
wbm = WestBendMutual(
    workers_comp=wbm[wbm["LOSS_KEY"]=="WC"].reset_index().drop("index",axis=1),
    prod_liab=wbm[wbm["LOSS_KEY"]=="PROD_LIAB"].reset_index().drop("index",axis=1),
    pp_auto=wbm[wbm["LOSS_KEY"]=="PP_AUTO"].reset_index().drop("index",axis=1),
    othr_liab=wbm[wbm["LOSS_KEY"]=="OTHR_LIAB"].reset_index().drop("index",axis=1),
    com_auto=wbm[wbm["LOSS_KEY"]=="COM_AUTO"].reset_index().drop("index", axis=1)
    )

sf  = StateFarm(
    workers_comp=sf[sf["LOSS_KEY"]=="WC"].reset_index().drop("index",axis=1),
    prod_liab=sf[sf["LOSS_KEY"]=="PROD_LIAB"].reset_index().drop("index",axis=1),
    pp_auto=sf[sf["LOSS_KEY"]=="PP_AUTO"].reset_index().drop("index",axis=1),
    othr_liab=sf[sf["LOSS_KEY"]=="OTHR_LIAB"].reset_index().drop("index",axis=1),
    com_auto=sf[sf["LOSS_KEY"]=="COM_AUTO"].reset_index().drop("index", axis=1)
    )

aeg = Aegis(
    pp_auto=aeg[aeg["LOSS_KEY"]=="PP_AUTO"].reset_index().drop("index",axis=1),
    othr_liab=aeg[aeg["LOSS_KEY"]=="OTHR_LIAB"].reset_index().drop("index",axis=1),
    com_auto=aeg[aeg["LOSS_KEY"]=="COM_AUTO"].reset_index().drop("index", axis=1)
    )


loss_data = {"wbm":wbm, "sf":sf, "aeg":aeg, "ta83":ta83, "raa":raa}
pkl_data_path = os.path.split(trikit.__file__)[0] + "\\datasets\\loss_data.pkl"
lrdb_path = os.path.split(trikit.__file__)[0] + "\\datasets\\lrdb.pkl"


with open(pkl_data_path, "wb") as f:
    pickle.dump(loss_data, f, pickle.HIGHEST_PROTOCOL)

with open(lrdb_path, "wb") as f:
    pickle.dump(lrdb, f, pickle.HIGHEST_PROTOCOL)





def load(dataset:str, **kwargs):
    """
    Load and return the dataset for the specified
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
    valid_datasets = ['raa','ta83','wbm','sf','aeg','lrdb']
    valid_lobs = ['workers_comp','prod_liab','pp_auto','othr_liab','com_auto']
    fdata = os.path.split(trikit.__file__)[0] + "\\datasets\\loss_data.pkl"
    flrdb = os.path.split(trikit.__file__)[0] + "\\datasets\\lrdb.pkl"
    dataset = dataset.lower().strip()


    fpath = flrdb if dataset=='flrdb' else fdata

    with open(fpath, 'rb') as f:

        data_kv = pickle.load(f)

        if dataset in valid_datasets:

            data = data_kv[dataset]

        else:

            raise ValueError("{} not a vaild dataset".format(dataset))


    # if   lob=="workers_comp": data = workers_comp
    #
    # elif lob=="prod_liab": data = prod_liab
    #
    # elif lob=="pp_auto": data = pp_auto
    #
    # elif lob=="other_liab": data = other_liab
    #
    # elif lob=="med_mal": data = med_mal
    #
    # elif lob=="com_auto": data = com_auto
    #
    # else:
    #
    #     raise KeyError("{} is not a valid key.".format(lob))

    # reset DataFrame index
    return(data.reset_index(inplace=True).drop("index", axis=1, inplace=True))

    return(data)

