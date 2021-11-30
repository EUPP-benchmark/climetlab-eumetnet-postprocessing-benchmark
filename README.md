# The Eumetnet postprocessing benchmark dataset Climetlab plugin

A dataset plugin for [climetlab](https://github.com/ecmwf/climetlab) for the Eumetnet postprocessing benchmark datasets.

Ease the download of time-aligned forecasts, reforecasts (hindcasts) and observations ([ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5)).

## Using climetlab to access the data

See the [demo notebooks](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?urlpath=lab)


- [demo_training_data_forecasts.ipynb](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_training_data_forecasts.ipynb)
  [![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb)
  [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/notebooks/demo_training_data_forecasts.ipynb)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Climdyn/climetlab-eumetnet-postprocessing-benchmark/main?filepath=notebooks/demo_training_data_forecasts.ipynb)
  [<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/tree/main/notebooks/demo_my_dataset.ipynb)


The climetlab python package allows easy access to the data with a few lines of code such as:
``` python
# Uncomment the line below if climetlab and the plugin are not yet installed
#!pip install climetlab climetlab-eumetnet-postprocessing-benchmark
import climetlab as cml
ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface', "2017-12-28", "2t", "hr")
ds.to_xarray()
```

## Datasets description

There are two main datasets: 

### 1 - Gridded Data


![](./docs/gridded_data.jpg)

 * The Eumetnet postprocessing benchmark dataset contains [ECMWF](https://www.ecmwf.int/) ensemble and deterministic forecasts over a large portion of Europe,  from 36 to 67° in latitude and from -6 to 17° of longitude,
and covers the years 2017-2018.

 * It also contains the corresponding ERA5 reanalysis for the purpose of providing observations for the benchmark.

 * For some dates, it contains also reforecasts that covers 20 years of past forecasts recomputed with the most recent model version.

 * All the forecasts and reforecasts provided are the noon ECMWF runs.

 * The gridded data resolution is 0.25° x 0.25° which corresponds roughly to 25 kilometers. 

 * **Please note that you can presently only retrieve one forecast date** for each `climetlab.load_dataset` call.

There are 5 gridded sub-datasets:

#### 1.1 - Extreme Forecast Index

All the [Extreme Forecast Index](https://www.ecmwf.int/assets/elearning/efi/efi1/story_html5.html) (EFI) variables can be obtained for each forecast date.

It includes:

| Parameter name                |  ECMWF key    |
|-------------------------------|---------------|
| 2 metre temperature efi     	|  2ti          |  
| 10 metre wind speed efi	    |  10ws         |
| 10 metre wind gust efi	    |  10fgi        |
| cape efi	                    |  capei        |
| cape shear efi	            |  capesi       |
| Maximum temperature at 2m efi	|  mx2ti        |
| Minimum temperature at 2m efi	|  mn2ti        |
| Snowfall efi	                |  sfi	        |
| Total precipitation efi	    |  tpi          |

**Usage**

The EFI variables can retrieved by calling 

``` python
ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-efi', date, parameter)
ds.to_xarray()
```

where the date argument is a string with a single date, and the parameter argument is a string or a list of string 

### 2 - Stations Data

Not yet provided.

## Major model changes

TODO

Support and contributing
------------------------

Please open a [issue on github](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/issues).

LICENSE
-------

See the [LICENSE](./LICENSE) file for the code, and the [DATA_LICENSE](./DATA_LICENSE) for the data.

Authors
-------

See the [CONTRIBUTORS.md](./CONTRIBUTORS.md) file.
