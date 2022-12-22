# The Eumetnet postprocessing benchmark dataset Climetlab plugin

[![PyPI version](https://badge.fury.io/py/climetlab-eumetnet-postprocessing-benchmark.svg)](https://badge.fury.io/py/climetlab-eumetnet-postprocessing-benchmark)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/climetlab-eumetnet-postprocessing-benchmark.svg)](https://pypi.org/project/climetlab-eumetnet-postprocessing-benchmark/)
[![build](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/actions/workflows/check-and-publish.yml/badge.svg?branch=main)](https://github.com/EUPP-benchmark/climetlab-eumetnet-postprocessing-benchmark/actions/workflows/check-and-publish.yml)
[<img src="https://img.shields.io/badge/docs-online-green.svg">](https://eupp-benchmark.github.io/EUPPBench-doc)

A plugin for [climetlab](https://github.com/ecmwf/climetlab) to retrieve the Eumetnet postprocessing benchmark datasets.

Ease the download of the dataset time-aligned forecasts, reforecasts (hindcasts) and observations ([ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5)).

> * **Climetlab plugin version**: 0.2.4
> * **EUPPBench dataset version**: 1.0
> * **Base dataset version**: 1.0
> * **Dataset status**: [Datasets status](https://eupp-benchmark.github.io/EUPPBench-doc/files/datasets_status.html#datasets-status)

## Documentation of the datasets

There are currently two sub-datasets available:

* [The EUPPBench dataset](https://eupp-benchmark.github.io/EUPPBench-doc/files/EUPPBench_datasets.html)
* [The base dataset over Europe's domain](https://eupp-benchmark.github.io/EUPPBench-doc/files/base_datasets.html)

They are both documented [here](https://eupp-benchmark.github.io/EUPPBench-doc/index.html).

## Using climetlab to access the data

See the [demo notebooks](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?urlpath=lab)


- [demo_training_data_forecasts.ipynb](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_training_data_forecasts.ipynb)
  [![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb)
  [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_training_data_forecasts.ipynb)
  [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_training_data_forecasts.ipynb)

- [demo_ensemble_forecasts.ipynb](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_ensemble_forecasts.ipynb)
  [![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_ensemble_forecasts.ipynb)
  [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_ensemble_forecasts.ipynb)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_ensemble_forecasts.ipynb)
  [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_ensemble_forecasts.ipynb)

- [demo_EUPPBench_germany_station_data.ipynb](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_germany_station_data.ipynb)
  [![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_germany_station_data.ipynb)
  [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_germany_station_data.ipynb)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_EUPPBench_germany_station_data.ipynb)
  [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_germany_station_data.ipynb)

- [demo_EUPPBench_gridded_data.ipynb](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_gridded_data.ipynb)
  [![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_gridded_data.ipynb)
  [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_EUPPBench_gridded_data.ipynb)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_EUPPBench_gridded_data.ipynb)
  [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_EUPPBench_gridded_data.ipynb)
 
The climetlab python package allows easy access to the data with a few lines of code such as:
``` python
# Uncomment the line below if climetlab and the plugin are not yet installed
#!pip install climetlab climetlab-eumetnet-postprocessing-benchmark
import climetlab as cml
ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface', "2017-12-02", "2t", "highres")
fcs = ds.to_xarray()
```
which download the deterministic (high-resolution) forecasts for the 2 metres temperature. 
Once obtained, the corresponding observations (if available) can be retrieved in the [xarray](http://xarray.pydata.org/en/stable/index.html) format by using the `get_observations_as_xarray` method:
``` python
obs = ds.get_observations_as_xarray()
```


## Support and contributing

Please open a [issue on github](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/issues).

## LICENSE

See the [LICENSE](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/LICENSE) file for the code, and the [DATA_LICENSE](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE) for the data.

## Authors

See the [CONTRIBUTORS.md](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/CONTRIBUTORS.md) file.
