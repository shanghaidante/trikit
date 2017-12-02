import pandas as pd
import numpy as np
# http://pandas.pydata.org/pandas-docs/stable/options.html
###############################################################################
# Pandas
###############################################################################

# create dataframe ===========================================================>
fdata1 = "U:\\Datasets\\Triangles_5_States.csv"

df = pd.read_csv(fdata1,
                 sep=",",
                 usecols=['POL_NBR','CLAIM_NO_10', 'LOC_NBR', 'ZIP5',
                          'LOCATION_ST', 'SIC5', 'CLASS_CD', 'CUSTOMER_SEGMENT',
                          'INDUSTRY', 'PROP_LIAB', 'COVERAGE', 'PERIL_TYPE',
                          'FIRE_CALIBRATION_LVL_OCC', 'LOSS_YR', 'DEV_PERIOD',
                          'INCRED_LOSS_NET_OF_SS_DED','PAID_LOSS_NET_OF_SS_AND_DED',
                          'ALAE', 'INCRD_ALAE_NET_OF_SS_AND_DED', 'CAT_IND', 'TIER',
                          'DISTRBN_BRANCH']
                 )


# rename columns =>
df.rename(columns={'FIRE_CALIBRATION_LVL_OCC':'OCC_LVL',
                   'INCRED_LOSS_NET_OF_SS_DED':'INCRD',
                   'PAID_LOSS_NET_OF_SS_AND_DED':'PAID',
                   'INCRD_ALAE_NET_OF_SS_AND_DED':'FREQ',
                   'DISTRBN_BRANCH':'BRANCH'},
          inplace=True)


# try query functionality and subset columns =>
vt = df.query("LOCATION_ST=='VT'")[['POL_NBR', 'CLAIM_NO_10', 'INDUSTRY', 'LOSS_YR', 'INCRD']]

self._dataset.groupby(['ORIGIN', 'DEV'],
                                               as_index=False).sum()




tn = df.query("LOCATION_ST='TN'")






# add a column to df =>
vt['TODAY'] = '20170609'

# rename 'FIRE_CALIBRATION_LVL_OCC'
#    'INCRED_LOSS_NET_OF_SS_DED'
# INCRD_ALAE_NET_OF_SS_AND_DED to freq
# DISTRBN_BRANCH => BRANCH


rdf = pd.DataFrame(np.random.random([3, 3]), columns=['A', 'B', 'C'])
rdf = pd.DataFrame(np.random.random([10, 5]), columns=['A', 'B', 'C', 'D', 'E'])
rdf = pd.DataFrame(np.random.random([8, 8]), columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])


# get shape of dataframe returns (rows, columns) =============================>
df.shape


# get columns ================================================================>
df.columns


# See the keys ===============================================================>
df.keys()

# See index ==================================================================>
df.index


# create empty dataframe =>
df_copy = pd.DataFrame(index=df_original.index,columns=df_original.columns)


# pivoting =>
df.pivot(index='date', columns='variable', values='value')


# groupby fields =>
grouped = df.groupby(['A', 'B'])


# filtering operations =>
df.loc[(df['column_name'] == some_value) & df['other_column'].isin(some_values)]
df.loc[df['column_name'].isin(some_values)]
df.loc[df['column_name'] == some_value]
df.loc[df['B'].isin(['one','three'])]
df[df['first_name'].notnull() & (df['nationality'] == "USA")]
df = df[(df['closing_price'] >= 99) & (df['closing_price'] <= 101)]
df = df[df['closing_price'].between(99, 101, inclusive=True)]


# using query method =========================================================>
f.query('99 <= closing_price <= 101')


# filter by index ============================================================>
df.loc[df.index < '2013-10-16 08:00:00']
df.ix[datetime.date(year=2014,month=1,day=1):datetime.date(year=2014,month=2,day=1)]
df['20160101':'20160301']



# set a cell to a value ======================================================>
df.set_value(<row>, <column>, <value>)
df.set_value('C', 'x', 10)
df[<column>][<row>] = 10    # modifies df itself
df['x']['C'] = 10

# using indicies only:
rdf.iloc[1, 1] = 7



# renaming columns =>
df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)


# drop a column ==============================================================>
# 1 is the axis number (0 for rows and 1 for columns.)
incr1 = df1.drop('PAID_LOSS_NET_OF_SS_AND_DED')
df.drop('column_name', axis=1, inplace=True)

# 1 is the axis number, first arg is column name:
rdf = rdf.drop(4, 1)


# drop a row =================================================================>
# ARB_IND  CNTR
# a   False   1.0
# b    True   2.0
# c   False   3.0
# d    True   4.0
# e    True   5.0
# 3     NaN   NaN

# to drop row 3 =>
df.drop(3, axis=0)   #axis=0 is optional
df.drop(1990)


# convert index to an actual column ==========================================>
df.reset_index(level=0, inplace=True)


# get unique values from column ==============================================>
df.name.unique()
df['FIELD'].unique()


# pivot columns ==============================================================>
df = df.pivot(index='newindex', columns='side').rename_axis(None)


# check if a row is in a list of values ======================================>
yrs = (2010, 2011)
incrd1 = incrd1[incrd1['ORIGIN'].isin(yrs)]


# get cumulative sum =========================================================>
df.cumsum(axis=1)
df.loc[:, '2':'3'].cumsum(axis=1)


# test if elements are null ==================================================>
df.isnull()


# get index of column known by label =========================================>
df.columns.get_loc(<label>)
df.columns.get_loc('C') # returns 3


# subsetting columns =========================================================>
df2 = df[['POL_NBR', 'CLAIM_NO_10', 'INDUSTRY', 'LOSS_YR', 'INCRD']]
df2 = df.iloc[:,:2]

# extract columns ============================================================>
df[['A','B']]; df[[1, 2]]
df['A']       # returns series
df[['A']]     # returns dataframe
df[[2]]     # returns 3rd column as dataframe
df.A

# select first 2 columns:
df.iloc[:,:2]

# identities to return entire row as series =>
df.loc[1985, :] == df.loc[1985]


# extract rows ===============================================================>
d.loc[[2]]           # get 3rd row as dataframe
d.loc[2]; d.iloc[2]  # get 3rd row as series

df.iloc[:3] # return rows 0, 1, 2
df.loc[:3]  # return rows 0, 1 ,2, 3
df[:3]      # return rows 0, 1, 2

df.iloc[0]  # returns 1st row

df.


# extract individal cells ====================================================>
df.iloc[<row>, <column>]
df.iloc[4, 3]

# using loc, refer to both the index and header name =>
df.loc['Utah', 'd']

# rows where deaths > 50:
df[df['deaths'] > 50]


# set value of a cell ========================================================>
df.set_value(row, col, value)
df.iloc[row, col] = value

df.iloc[1, 2] = np.nan

# select all rows by index label =============================================>
df.loc[:'Arizona']

# fill 2nd column na values with 0 ===========================================>
df[2].fillna(0, inplace=True)


# replace 0.0 with NaN =======================================================>
ti1.iloc[:1].replace(0.0, np.nan)



# sum over all rows or all columns ===========================================>
df.sum(0) # over rows
df.sum(1) # over columns



# convert Series to DataFrame ================================================>
sd = s.to_frame(name='FIELDNAME')


# find first and last valid index ============================================>
Series.first_valid_index()
Series.last_valid_index()


# misc manipulations =========================================================>
# [1] => Sum value over unique combinations of ORIGIN and DEV =>
incrd1 = incrd1.groupby(['ORIGIN', 'DEV'], as_index=False).sum()
paid1  = paid1.groupby(['ORIGIN', 'DEV'], as_index=False).sum()
alae1  = alae1.groupby(['ORIGIN', 'DEV'], as_index=False).sum()


# [2] => Transpose DEV into columns:
ti1 = incrd1.pivot(index='ORIGIN', columns='DEV').rename_axis(None)
tp1 = paid1.pivot(index='ORIGIN', columns='DEV').rename_axis(None)
ta1 = alae1.pivot(index='ORIGIN', columns='DEV').rename_axis(None)

ti1.replace(0.0, np.NaN, inplace=True)
tp1.replace(0.0, np.NaN, inplace=True)
ta1.replace(0.0, np.NaN, inplace=True)


# [3] => Create cumulative triangle =>
tic = ti1.cumsum(axis=1)
tpc = tp1.cumsum(axis=1)
tac = ta1.cumsum(axis=1)

Series.first_valid_index()
Series.last_valid_index()


# apply a function over a dataframe ==========================================>

# ===================================================
# Difference between `map`, `apply` & `applymap`    |
# ===================================================
# apply works on a row/column basis of a DataFrame
# applymap works element-wise on a DataFrame
# map works element-wise on a Series


# map:
#     iterates over each element of a series:
#
#     df[‘column1’].map(lambda x: 10+x)
#     df[‘column2’].map(lambda x: ‘AV’+x)
#
#
# apply:
#     applies a function along any axis of the DataFrame:
#
#     df[[‘column1’,’column2’]].apply(sum)


df = pd.DataFrame(
        np.random.randn(4, 3),
        columns=list('bde'),
        index=['Utah', 'Ohio', 'Texas', 'Oregon']
        )

df = df.applymap(np.exp)


# to modify column 'b', returning the entire modified dataframe =>
df['b'] = df['b'].apply(lambda x: 10*x)
df['b'] = df['b'].map(lambda x: 10*x)


# apply function across columns of dataframe:
df.loc[['Utah']] = df.loc[['Utah']].apply(lambda x: x*x)










# apply() can apply a function along any axis of the dataframe =>
#   axis 0 => row
#   axis 1 => column












# if index is not a integer, get it's position ===============================>
df.index.get_loc('c')



# test 2 DataFrame's for equality ============================================>
df1['VALUE'].sum()==df2['VALUE'].sum()

# join 2 dataframes ==========================================================>
pd.set_option('precision', 10)
pd.set_option('display.chop_threshold', None)


df1 = pd.DataFrame({'A' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                    'B' : [np.random.random() for i in range(10)],
                    'C' : pd.Categorical(['test', 'train', 'test', 'train', 'test']*2),
                    'D' : ['AAA', 'BBB', 'CCC', 'AAA', 'BBB', 'CCC', 'AAA', 'BBB', 'CCC', 'AAA'],
                    'E' : [random.randint(1000, 1005) for i in range(10)],
                    'F' : 2.})


df2 = pd.DataFrame({'A' : ['A', 'B', 'C'],
                    'G' : 1.0,
                    'H' : 'St. Laurence',
                    'I' : [111, 222, 333]})


# merge(left, right, how='left', on=None, left_on=None, right_on=None,
#       left_index=False, right_index=False, sort=True,
#       suffixes=('_x', '_y'), copy=True)
df = pd.merge(df1, df2, how='left', on='A')

###############################################################################


rdf = pd.DataFrame(np.random.random([8, 8]),
                   columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
nrows  = rdf.shape[0]
ncols  = rdf.shape[1]
hdrpos = list(rdf.columns.values)

# df.set_value(<row>, <column>, <value>)


for i in range(nrows):

    for j in range(ncols):

        iterhdr = hdrpos[j]

        if j >= (ncols - i):
            rdf.set_value(i, iterhdr, np.NaN)

        if i==0 and iterhdr=='E':
            rdf.set_value(i, iterhdr, np.NaN)

        if i==0 and iterhdr=='F':
            rdf.set_value(i, iterhdr, np.NaN)

        if i==3 and iterhdr=='C':
            rdf.set_value(i, iterhdr, np.NaN)

        if i==3 and iterhdr=='D':
            rdf.set_value(i, iterhdr, np.NaN)

        if i==1 and iterhdr=='F':
            rdf.set_value(i, iterhdr, np.NaN)

        if i==2 and iterhdr=='E':
            rdf.set_value(i, iterhdr, np.NaN)



# logic for making in-between NaN's 0 for cumulation =>
for i in range(nrows):
    iterupto = (len(rdf.columns) - i)
    for j in range(ncols):
        iterval = rdf.iloc[i, j]
        if j < iterupto:
            if np.isnan(iterval): rdf.iloc[i, j] = 0

cdf = rdf.cumsum(axis=1)


# DataFrame construction =====================================================>

df = pd.DataFrame({ 'A' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                    'B' : [np.random.random() for i in range(10)],
                    'C' : pd.Categorical(['test', 'train', 'test', 'train', 'test']*2),
                    'D' : ['AAA', 'BBB', 'CCC', 'AAA', 'BBB', 'CCC', 'AAA', 'BBB', 'CCC', 'AAA'],
                    'E' : [random.randint(1000, 1005) for i in range(10)],
                    'F' : 1.})


# create from dict:

d1 = pd.Series({'a':1, 'b':2, 'c':3, 'd':4, 'e':5})
d2 = pd.Series({'a':False, 'b':True, 'c':False, 'd':True, 'e':True})
d  = pd.DataFrame({'CNTR':d1, 'ARB_IND':d2})
type(d)
d.shape



###############################################################################
# loc works on labels in the index.

# iloc works on the positions in the index (so it only takes integers).


# loc => works on labels in the index
# iloc => works on the positions in the index (so it only takes integers)
# ix: You can get data from dataframe without it being in the index
# at: get scalar values. It's a very fast loc
# iat: Get scalar values. It's a very fast iloc


# NOTES:
df = pd.DataFrame({
        'A':[1,2,3,4,5],
        'B':['a','b','a','b','a'],
        'C':[5,4,3,2,np.NaN],
        'D':[np.NaN,np.NaN,np.NaN,7,-1]
        })

df = pd.DataFrame({
        'A':[1,2,3,4,5],
        'C':[5,4,3,2,np.NaN],
        'D':[np.NaN,np.NaN,np.NaN,7,-1]
        })




import numpy as np
import pandas as pd
import collections
import datetime
curr_yr = datetime.datetime.today().strftime('%Y')
results = collections.OrderedDict()
accident_years = 10
init_accident_year = int(curr_yr)-accident_years
index = list(range(init_accident_year, int(curr_yr)))
for i in range(accident_years):
    iterarr = np.random.lognormal(10, .5, accident_years-i).tolist()
    iterarr.extend([np.NaN]*i)
    results[i] = iterarr

inc = pd.DataFrame(data=results, index=index)




inc = pd.DataFrame({
        1 :results[0],
        2 :results[1],
        3 :results[2],
        4 :results[3],
        5 :results[4],
        6 :results[5],
        7 :results[6],
        8 :results[7],
        9 :results[8],
        10:results[9]}, index=index)










df = pd.DataFrame({
    'A':[1,2,3,4,5],
    'B':[3,5,7,9,np.NaN],
    'C':[11,13,15,np.NaN,np.NaN],
    'D':[2,4,np.NaN,np.NaN,np.NaN],
    'E':[8,np.NaN,np.NaN,np.NaN,np.NaN]
    })

df = pd.DataFrame({
        'A':[1,2,3,4,5],
        'B':['a','b','a','b','a'],
        'C':[5,4,3,2,np.NaN],
        'D':[np.NaN,np.NaN,np.NaN,7,-1]
        })

df = pd.DataFrame(
        np.random.randn(4, 3),
        columns=list('bde'),
        index=['Utah', 'Ohio', 'Texas', 'Oregon']
        )


without `iloc`, slicing works on rows:
df[:1]
         b         d        e
Utah -0.062962 -0.274263  0.21066


`iloc` slices rows and columns For example, consider:


              b         d         e
Utah   -0.062962 -0.274263  0.210660
Ohio    0.111679 -0.118416 -0.127113
Texas   0.593764 -0.065196 -0.673432
Oregon -0.293202 -0.395619  0.446270


Calling df[:2] returns:

             b         d         e
    Utah -0.062962 -0.274263  0.210660
    Ohio  0.111679 -0.118416 -0.127113


Calling df[:1] returns:

                b         d        e
    Utah -0.062962 -0.274263  0.21066



to return first column:

    df[[0]]
    df.iloc[:, 0]


using loc:
df.loc['Utah']

returns Series =>
    b   -0.062962
    d   -0.274263
    e    0.210660


df.loc[['Utah']]

returns DataFrame =>
                b         d        e
    Utah -0.062962 -0.274263  0.21066



# For pandas objects (Series, DataFrame), the indexing operator [] only
# accepts:
#
#     * colname or list of colnames to select column(s)
#     * slicing or Boolean array to select row(s), i.e. it only refers to one
#       dimension of the dataframe.
#
#
# For df[[colname(s)]], the interior brackets are for list, and the outside brackets
# are indexing operator, i.e. you must use double brackets if you select two or
# more columns. With one column name, single pair of brackets returns a Series,
# while double brackets return a dataframe.


# Populate a column looking up values from a dict =>
equiv = {7001:1, 8001:2, 9001:3}
df = pd.DataFrame( {"A": [7001, 8001, 9001]} )
df["B"] = df["A"].map(equiv)