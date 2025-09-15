EUPreciPBench datasets
======================

The *EUPreciPBench* datasets are available on a small portion of Europe stored in `Zarr <https://zarr.readthedocs.io/en/stable/>`_
format for an easy access allowing for slicing.
The forecasts and observations datasets are already paired together, providing analysis-ready data
for postprocessing benchmarking purposes.

It is a forecasts and observations dataset on a regular latitude-longitude grid, containing *high-resolution* precipitation data,
along with some predictors in the column above the surface. It's horizontal resolution is higher (0.025°) than the one of
the :ref:`files/EUPPBench_datasets:EUPPBench datasets` (0.25°), but they are conveniently defined on the same domain.

.. figure:: ../images/gridded_data_EUPP.jpg
    :scale: 70%
    :align: center

    In blue, the EUPreciPBench dataset domain inside the :ref:`files/base_datasets:Base datasets over Europe's domain`.

-  The gridded EUPPreciBench postprocessing benchmark dataset contains
   `COSMO`_ DE and D2 ensemble forecasts over a small domain in Europe, from 46.0° to 53.2° in latitude, and from 2.5° to 10.4° in longitude,
   and covers the years 2017-2020.
-  It also contains the corresponding `EURADCLIM`_ radar composite for the purpose of
   providing observations for the benchmark.
-  The forecasts provided are the COSMO runs initialized at 03Z.
-  The COSMO ensemble consists of 20 members.
-  The gridded data resolution is 0.025° x 0.025° which corresponds
   roughly to 2.5 kilometers. COSMO DE, D2 and EURADCLIM data have been regridded to this resolution from their native grid.
-  COSMO DE forecasts (prior to May 2018) only covers part of the EUPPBench domain. COSMO D2 forecasts cover the full EUPPBench domain.
-  Forecasts are hourly, up to 2 days ahead, but do not include the analysis at 03Z.


Datasets description
--------------------

There are 3 gridded sub-datasets:

1 - Precipitation Forecasts Data
--------------------------------

It consists in the total precipitation variable accumulated in the past hour:

+----------------------------------------------+-----------+---------+---------+
| Parameter name                               | ECMWF key | Units   | Remarks |
+==============================================+===========+=========+=========+
| `Total                                       | tp        | mm      |         |
| precipitation <https://ap                    |           |         |         |
| ps.ecmwf.int/codes/grib/param-db/?id=228>`__ |           |         |         |
+----------------------------------------------+-----------+---------+---------+

.. warning::

   The units for the total precipitation here are not consistent with the :ref:`files/EUPPBench_datasets:EUPPBench datasets`
   total precipitation units. As the latter uses meters as units, there is a factor 1000 between the two.

**Usage:** The precipitation forecasts can be retrieved by calling

.. code:: python

   import climetlab as cml
   ds = cml.load_dataset('EUPreciPBench-gridded-precipitation-forecasts')
   ds.to_xarray()

Alternatively, one can use the `Intake catalogue`_

.. code:: python

   import euppbench_datasets
   cat = euppbench_datasets.open_catalog()
   ds = cat.euprecipbench.EUPreciPBench_precipitation_forecasts.to_dask()

**Example:**

.. jupyter-execute::

   import climetlab as cml
   ds = cml.load_dataset('EUPreciPBench-gridded-precipitation-forecasts')
   ds.to_xarray()

2 - Predictors Forecasts Data
-----------------------------

It consists of several forecasts fields on pressure levels:

+-------------------------------------+---------------+-----------+---------+---------+
| Parameter name                      | Levels        | ECMWF key | Units   | Remarks |
+=====================================+===============+===========+=========+=========+
| `Temperature <https://apps.ecmwf.   | 500, 700, 850 | t         | K       |         |
| int/codes/grib/param-db/?id=130>`__ |               |           |         |         |
+-------------------------------------+---------------+-----------+---------+---------+
| `U component of                     | 700, 950      | u         | m s^-1  |         |
| wind <https://apps.ecmwf.           |               |           |         |         |
| int/codes/grib/param-db/?id=131>`__ |               |           |         |         |
+-------------------------------------+---------------+-----------+---------+---------+
| `V component of                     | 700, 950      | v         | m s^-1  |         |
| wind <https://apps.ecmwf.           |               |           |         |         |
| int/codes/grib/param-db/?id=132>`__ |               |           |         |         |
+-------------------------------------+---------------+-----------+---------+---------+
| `Relative                           | 700, 850, 950 | r         | %       |         |
| humidity <https://apps.ecmwf.       |               |           |         |         |
| int/codes/grib/param-db/?id=157>`__ |               |           |         |         |
+-------------------------------------+---------------+-----------+---------+---------+

These fields can for example be used to compute the `Jefferson instability index`_ and used
as predictors for postprocessing the precipitation ensemble forecasts.

**Usage:** The predictors forecasts can be retrieved by calling

.. code:: python

   import climetlab as cml
   ds = cml.load_dataset('EUPreciPBench-gridded-predictors-forecasts')
   ds.to_xarray()

Alternatively, one can use the `Intake catalogue`_

.. code:: python

   import euppbench_datasets
   cat = euppbench_datasets.open_catalog()
   ds = cat.euprecipbench.EUPreciPBench_predictors_forecasts.to_dask()

**Example:**

.. jupyter-execute::

   ds = cml.load_dataset('EUPreciPBench-gridded-predictors-forecasts')
   ds.to_xarray()

3 - Precipitation Observations Data
-----------------------------------

It consists in the total precipitation variable accumulated in the past hour:

+----------------------------------------------+-----------+---------+---------+
| Parameter name                               | ECMWF key | Units   | Remarks |
+==============================================+===========+=========+=========+
| `Total                                       | tp        | mm      |         |
| precipitation <https://ap                    |           |         |         |
| ps.ecmwf.int/codes/grib/param-db/?id=228>`__ |           |         |         |
+----------------------------------------------+-----------+---------+---------+

.. warning::

   The units for the total precipitation here are not consistent with the :ref:`files/EUPPBench_datasets:EUPPBench datasets`
   total precipitation units. As the latter uses meters as units, there is a factor 1000 between the two.

**Usage:** The precipitation observations can be retrieved by calling

.. code:: python

   import climetlab as cml
   ds = cml.load_dataset('EUPreciPBench-gridded-precipitation-observations')
   ds.to_xarray()

Alternatively, one can use the `Intake catalogue`_

.. code:: python

   import euppbench_datasets
   cat = euppbench_datasets.open_catalog()
   ds = cat.euprecipbench.EUPreciPBench_EURADCLIM_observations.to_dask()

**Example:**

.. jupyter-execute::

   ds = cml.load_dataset('EUPreciPBench-gridded-precipitation-observations')
   ds.to_xarray()

4 - Static fields
-----------------

Various static fields associated to the forecast grid can be obtained,
with the purpose of serving as predictors for the postprocessing.

.. note::

   For consistency with the rest of the dataset, we use the
   ECMWF parameters name, terminology and units here. However, please
   note that - except for the Surface Geopotential - the fields provided are from other non-ECMWF data sources
   evaluated at grid points. Currently, the main data source being used
   is the `Copernicus Land Monitoring
   Service <https://land.copernicus.eu/>`__.

It includes:

+---------------------------------------------------------------------------------+-----------+-------------------------------------------------------------------------------------------------------------+
| Parameter name                                                                  | ECMWF key | Remarks                                                                                                     |
+=================================================================================+===========+=============================================================================================================+
| `Land use <https://apps.ecmwf.int/codes/grib/param-db/?id=260184>`_             | landu     | Extracted from the `CORINE 2018`_ dataset.                                                                  |
|                                                                                 |           | Values and associated land type differ from the ECMWF one.                                                  |
|                                                                                 |           | Please look at the “legend” entry in the metadata for more details.                                         |
+---------------------------------------------------------------------------------+-----------+-------------------------------------------------------------------------------------------------------------+
| `Model terrain height <https://apps.ecmwf.int/codes/grib/param-db/?id=260183>`_ | mterh     | Extracted from the `EU-DEMv1.1 <https://land.copernicus.eu/imagery-in-situ/eu-dem>`__ data elevation model  |
|                                                                                 |           | dataset.                                                                                                    |
+---------------------------------------------------------------------------------+-----------+-------------------------------------------------------------------------------------------------------------+
| `Surface Geopotential <https://apps.ecmwf.int/codes/grib/param-db/?id=129>`_    | z         | The model orography can be obtained by dividing the surface geopotential by g=9.80665 ms :math:`{}^{-2}`.   |
+---------------------------------------------------------------------------------+-----------+-------------------------------------------------------------------------------------------------------------+

**Usage:** The static fields can be retrieved by calling

.. code:: python

   ds = cml.load_dataset('EUPreciPBench-gridded-static-fields', parameter)
   ds.to_xarray()

where the ``parameter`` argument is a string with one of the ECMWF keys
described above. It is only possible to download one static field per
call.

Alternatively, one can use the `Intake catalogue`_

.. code:: python

   import euppbench_datasets
   cat = euppbench_datasets.open_catalog()
   # Fetching the land usage field
   ds = cat.euprecipbench.EUPreciPBench_land_usage.to_dask()

The other static field are also available in the same way.

**Example:**

.. jupyter-execute::

   ds = cml.load_dataset('EUPreciPBench-gridded-static-fields', 'landu')
   ds.to_xarray()


5 - Explanation of the metadata
-------------------------------

For all data, attributes specifying the sources and the license are always present.
Depending on the kind of dataset, dimensions and information are embedded in the data as follow:

+-------------------------------------+----------------------------------------------------------------------+
| Metadata                            | Description                                                          |
+=====================================+======================================================================+
|  **latitude**                       | Latitude of the grid points.                                         |
+-------------------------------------+----------------------------------------------------------------------+
|  **longitude**                      | Longitude of the grid points.                                        |
+-------------------------------------+----------------------------------------------------------------------+
|  **number**                         | Number of the ensemble member.                                       |
+-------------------------------------+----------------------------------------------------------------------+
|  **time**                           | Forecast initialization date                                         |
+-------------------------------------+----------------------------------------------------------------------+
|  **step**                           | Step of the forecast (the lead time).                                |
+-------------------------------------+----------------------------------------------------------------------+
|  **surface**                        | Layer of the variable considered                                     |
|                                     | (here there is just one, at the surface).                            |
+-------------------------------------+----------------------------------------------------------------------+
|   **isobaricInhPa**                 | Pressure level in hectopascal (or millibar).                         |
+-------------------------------------+----------------------------------------------------------------------+
|   valid_time                        | Actual time and date of the corresponding forecast data.             |
+-------------------------------------+----------------------------------------------------------------------+

.. note::

   **Bold** metadata denotes dimensions indexing the datasets.

Data License
------------

See the
`DATA_LICENSE <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE>`__ file.

The COSMO forecasts were produced and provided by the Deutsche Wetterdienst (DWD).
The EURADCLIM were produced and provided by KNMI. See https://dataplatform.knmi.nl/dataset/rad-opera-hourly-rainfall-accumulation-euradclim-2-0 and
https://doi.org/10.5194/essd-15-1441-2023 .

.. _COSMO: https://www.dwd.de/EN/research/weatherforecasting/num_modelling/01_num_weather_prediction_modells/regional_model_cosmo_de.html;jsessionid=78803A010B98F465DA4E8F26975933C6.live31082?nn=484268
.. _EURADCLIM: https://dataplatform.knmi.nl/dataset/rad-opera-hourly-rainfall-accumulation-euradclim-2-0
.. _Intake catalogue: https://github.com/EUPP-benchmark/intake-eumetnet-postprocessing-benchmark
.. _Jefferson instability index: https://adgeo.copernicus.org/articles/7/131/2006/
.. _CORINE 2018: https://land.copernicus.eu/pan-european/corine-land-cover

