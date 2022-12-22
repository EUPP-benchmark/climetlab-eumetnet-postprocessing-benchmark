.. The Eumetnet postprocessing benchmark dataset Climetlab plugin documentation master file, created by
   sphinx-quickstart on Wed Nov 16 09:51:42 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The EUPP postprocessing benchmark dataset documentation
=======================================================

This website document the EUMETNET postprocessing benchmark datasets, an initiative to provide high-quality datasets to derive
easily analysis-ready datasets that can be used to perform benchmarking tasks of weather forecast postprocessing methods.

The main tool to download and manage the data is a Python plugin. It can however convert the data to formats that can
then be processed by other languages, and a few line of Python codes suffice to obtain the datasets.


.. note::

   * **Climetlab plugin version**: 0.2.4
   * **EUPPBench dataset version**: v1.0
   * **Base dataset version**: v1.0
   * **Dataset status**: :ref:`files/datasets_status:Datasets status`

.. toctree::
   :maxdepth: 1
   :caption: Currently available datasets:

   files/EUPPBench_datasets
   files/base_datasets

Using climetlab to access the data
----------------------------------

A plugin for `climetlab <https://github.com/ecmwf/climetlab>`__ to
retrieve the Eumetnet postprocessing benchmark datasets is available.

|PyPI version| |PyPI pyversions| |build|

It facilitates the download of the dataset time-aligned forecasts, reforecasts
(hindcasts) and observations (`ERA5
reanalysis <https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5>`__).

See the `demo
notebooks <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks>`__
|Binder|

-  `demo_training_data_forecasts.ipynb <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_training_data_forecasts.ipynb>`__
   |nbviewer| |Open in colab| |image1| |image6|

-  `demo_ensemble_forecasts.ipynb <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_ensemble_forecasts.ipynb>`__
   |image2| |image3| |image4| |image7|

-  `demo_EUPPBench_germany_station_data.ipynb <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_germany_station_data.ipynb>`__
   |image15| |image16| |image17| |image21|

-  `demo_EUPPBench_gridded_data.ipynb <https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_gridded_data.ipynb>`__
   |image18| |image19| |image20| |image22|

The climetlab python plugin allows users to easily access the data with a few
lines of code such as:

.. code:: python

   # Uncomment the line below if climetlab and the plugin are not yet installed
   #!pip install climetlab climetlab-eumetnet-postprocessing-benchmark
   import climetlab as cml
   ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface', "2017-12-02", "2t", "highres")
   fcs = ds.to_xarray()

which for instance download the deterministic (high-resolution) forecasts for the 2
metres temperature.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |PyPI version| image:: https://badge.fury.io/py/climetlab-eumetnet-postprocessing-benchmark.svg
   :target: https://badge.fury.io/py/climetlab-eumetnet-postprocessing-benchmark
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/climetlab-eumetnet-postprocessing-benchmark.svg
   :target: https://pypi.org/project/climetlab-eumetnet-postprocessing-benchmark/
.. |build| image:: https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/actions/workflows/check-and-publish.yml/badge.svg?branch=main
   :target: https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/actions/workflows/check-and-publish.yml
.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?urlpath=lab
.. |nbviewer| image:: https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg
   :target: https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb
.. |Open in colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb
.. |image1| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_training_data_forecasts.ipynb
.. |image2| image:: https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg
   :target: https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_ensemble_forecasts.ipynb
.. |image3| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_ensemble_forecasts.ipynb
.. |image4| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_ensemble_forecasts.ipynb
.. |image6| image:: https://deepnote.com/buttons/launch-in-deepnote-small.svg
   :target: https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_training_data_forecasts.ipynb
.. |image7| image:: https://deepnote.com/buttons/launch-in-deepnote-small.svg
   :target: https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_ensemble_forecasts.ipynb
.. |image15| image:: https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg
   :target: https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_germany_station_data.ipynb
.. |image16| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_germany_station_data.ipynb
.. |image17| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_EUPPBench_germany_station_data.ipynb
.. |image18| image:: https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg
   :target: https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_gridded_data.ipynb
.. |image19| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_gridded_data.ipynb
.. |image20| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_EUPPBench_gridded_data.ipynb
.. |image21| image:: https://deepnote.com/buttons/launch-in-deepnote-small.svg
   :target: https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_germany_station_data.ipynb
.. |image22| image:: https://deepnote.com/buttons/launch-in-deepnote-small.svg
   :target: https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_gridded_data.ipynb
