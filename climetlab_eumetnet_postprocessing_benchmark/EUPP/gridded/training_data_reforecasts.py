#!/usr/bin/env python3
from __future__ import annotations

from .training_data_forecasts import TrainingDataForecastSurface, TrainingDataForecastPressure,\
    TrainingDataForecastSurfacePostProcessed

__version__ = "0.2.2"


class TrainingDataReforecastSurface(TrainingDataForecastSurface):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = "data/gridded_data/gridded_{kind}_reforecasts_surface.zarr"

    def __init__(self):

        TrainingDataForecastSurface.__init__(self, "ensemble")


class TrainingDataReforecastPressure(TrainingDataForecastPressure):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    _PATTERN = "data/gridded_data/gridded_{kind}_reforecasts_pressure_{level}.zarr"

    dataset = None

    def __init__(self, level):

        TrainingDataForecastPressure.__init__(self, level, "ensemble")


class TrainingDataReforecastSurfacePostProcessed(TrainingDataForecastSurfacePostProcessed):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    _PATTERN = "data/gridded_data/gridded_{kind}_reforecasts_surface_postprocessed.zarr"

    dataset = None

    def __init__(self):

        TrainingDataForecastSurfacePostProcessed.__init__(self, "ensemble")

