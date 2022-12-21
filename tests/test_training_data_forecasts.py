#!/usr/bin/env python3

import climetlab as cml
import numpy as np
# TODO: test values


def test_efi():
    ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-efi',
                          date="2017-12-28",
                          parameter="2ti")
    xds = ds.to_xarray()
    print(xds)


def test_fcs_surf():
    ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface',
                          date="2017-12-28",
                          parameter="2t",
                          kind="highres")
    xds = ds.to_xarray()
    obs = ds.get_observations_as_xarray()
    assert xds.t2m.shape == obs.t2m.shape
    assert np.all(xds.time == obs.time)
    assert np.all(xds.valid_time == obs.valid_time)


def test_fcs_press():
    ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-pressure',
                          date="2017-12-28",
                          parameter="z",
                          level=500,
                          kind="ensemble")
    xds = ds.to_xarray()
    obs = ds.get_observations_as_xarray()
    assert xds.z.shape[1:] == obs.z.shape[1:]
    assert np.all(xds.time == obs.time)
    assert np.all(xds.valid_time == obs.valid_time)


def test_fcs_pp():
    ds = cml.load_dataset("eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface-processed",
                          date="2017-12-28",
                          parameter=["mx2t6"],
                          kind="hr")
    xds = ds.to_xarray()
    obs = ds.get_observations_as_xarray()
    assert xds.mx2t6.shape[1:] == obs.mx2t6.shape[1:]
    assert np.all(xds.time == obs.time)
    assert np.all(xds.valid_time == obs.valid_time)
    assert not np.any(np.isnan(obs.mx2t6))


if __name__ == "__main__":
    test_efi()
    test_fcs_surf()
    test_fcs_press()
    test_fcs_pp()
