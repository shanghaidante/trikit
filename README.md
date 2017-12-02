# Introduction
The `trikit` package is a collection of Loss Reserving tools and techniques
created for the purpose of simplifying Actuarial analyses in Python, with
particular focus on automating the basic techniques generally used for
estimating unpaid claim liabilities. `trikit` current implements the Chain
Ladder (or *development*) method for ultimate loss projection, as well as
techniques to estimate the error in Chain Ladder estimates via the Mack and
Bootstrap methods.
<br>
In addition to tools and techniques, `trikit` is shipped with sample
datasets that can be used to gain familiarity with the package's interface.
`trikit.datasets` contains data from the [Casualty Actuarial Society's Loss
Reserving Datasets](http://www.casact.org/research/index.cfm?fa=loss_reserves_data)
compiled and maintained by Glenn Meyers. These datasets have been aggregated
over carrier and partitioned by industry, and include paid and reported losses
for the following lines of business:

*  Workers Compensation
*  Products Liability
*  Personal Passenger Auto
*  Other Liability
*  Medical Malpractice
*  Commercial Auto

Any of these datasets can be loaded into Python by calling the `load` function,
which takes an optional `lob` keyword. `lob` is set to Workers Compensation
by default, but can be instructed to load any of the other datasets by
providing its associated `lob` argument:

|Line of Business         |`lob` Argument |
|:-----------------------:|:-------------:|
|Workers Compensation     |`workers_comp` |
|Products Liability       |`prod_liab`    |
|Personal Passenger Auto  |`pp_auto`      |
|Other Liability          |`other_liab`   |
|Medical Malpractice      |`med_mal`      |
|Commercial Auto          |`com_auto`     |
|                         |               |
<br>
For example, to load the 'Other Liability' dataset into Python, we'd run:
<br>
```python
>>> import trikit
>>> othrliab = trikit.load(lob="other_liab")
>>> type(othrliab)
pandas.core.frame.DataFrame
>>> othrliab.head

   ORIGIN  DEV_PERIOD  INCRD_LOSS
0    1988           1      295980
1    1988           2      315210
2    1988           3      338804
3    1988           4      363137
4    1988           5      346240

```
<br>
Once the dataset has been loaded, it's straightforward to transform incremental
losses into a `Triangle` type. Three arguments need to be provided: The origin
year (or accident year) as `origin`, the development period as `dev` and the
loss amount of interest as `value`. Referring again to the 'Other Liability'
sample dataset, `_Incremental` and `_Cumulative` triangle types are initialized
as follows:
<br>
```python
# initializing Incremental and Cumulative triangles
# from 'Other Liability' builtin dataset:
>>> import trikit
>>> othrliab = trikit.load(lob="other_liab")
>>> inc = trikit._Incremental(othrliab, origin="ORIGIN", dev="DEV", value="VALUE")
>>> cum = trikit._Cumulative(othrliab, origin="ORIGIN", dev="DEV", value="VALUE")
>>> type(inc)
trikit.triangle._Incremental
>>> type(cum)
trikit.triangle._Cumulative

```

Initializing incremental or cumulative triangles from data from file is just
as easy. Provide the name of the delimited datafile as the first
argument to the constructor, along with the file delimiter (optional):
<br>
```python
# initializing triangles from file
>>> import trikit
>>> tri_data = "path/to/triangle_data.csv"
>>> inc = trikit._Incremental(tri_data, sep=",", origin="ORIGIN", dev="DEV", value="VALUE")
>>> cum = trikit._Cumulative(tri_data, sep=",", origin="ORIGIN", dev="DEV", value="VALUE")
>>> type(inc)
trikit.triangle._Incremental
>>> type(cum)
trikit.triangle._Cumulative

```



























Note that the datasets distirubted
with `trikit` do not include squared triangle data but only contain the
incremental losses aggregated over carrier and partitioned by industry






















## The `BaseTriangle` Class
`trikit` is built around the `BaseTriangle` type, which wraps
`pandas.DataFrame` and comes in both `Incremental` and `Cumulative`
varieties:

*  `Incremental`: Refers to the sum of all claim payments made during a
    specified time interval.
<br>
*  `Cumulative`: Refers to the sum of all claim payments through a given
   valuation date.
<br>


























`BaseTriangle` type, which encompasses all the functionality exposed by the
pandas Data.Frame  and in both `Incremental` and `Cumulative` varieties.






addition to the base Incremental and Cumulative loss triangle classes, `trikit`
exposes a collection of

exposes functionality intended to simplify Loss Triangle-
based


The `BaseTriangle` class transforms tabular data into an incremental loss
triangle, with development periods running horizontally (increasing
from left to right) and origin period (typically year) running
vertically (increasing from top to bottom). To illustrate:

```
            Increasing Development Period =====>

            Typically:
                `1` =>  0-12 Months
                `2` => 12-24 Months
                `3` => 24-36 Months, etc...

           ==============================================
Increasing |****|   1   |   2   |   3   |   4   |   5   |
Origin     ==============================================
 Year      |2012| 1065    2793    1875    2211    1287  |
  ||       |2013|  942    1232    1179    1514     NaN  |
  ||       |2014| 1334    1887    1665     NaN     NaN  |
  ||       |2015| 1774    2173     NaN     NaN     NaN  |
  \/       |2016| 2229     NaN     NaN     NaN     NaN  |
           ==============================================
```

Assuming the sample triangle contains incremental paid losses, the 1875 dollar
amount in cell (2012, 3) represents losses paid between 24-36 months after the
claim was reported (sometime in 2014).

In order to create an instance of the Triangle class, it is necessary to
provide, at a minimum, the fieldnames from the dataset that correspond to Loss
Year (the `origin` argument), Development Period (the `dev` argument) and Loss
Amount (the `value` argument). Note that **kwargs represents a collection of
keyword arguments that permit specifying multiple fields in the referenced
dataset, so that triangles can be generated for multiple types of loss
simultaneously: For example, claim datasets typically contain reported claims,
paid claims and ALAE, in addition to paid and reported claim counts. It is
possible to pass to the Triangle class constuctor a dictionary which maps the
fieldnames specific to the dataset to a corresponding user-defined handle. The
only requirement is that 'origin' correspond to the key for loss year, and
'dev' corresponds to the key for development period.

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
