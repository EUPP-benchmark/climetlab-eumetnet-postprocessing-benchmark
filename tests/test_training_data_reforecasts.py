#!/usr/bin/env python3

import climetlab as cml


def test_rfcs_surf():
    ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-reforecasts-surface',
                          date="2017-12-28",
                          parameter="2t")
    xds = ds.to_xarray()
    obs = ds.get_observations_as_xarray()
    print(xds)
    print(obs)
    assert xds.t2m.shape == obs.t2m.shape


def test_rfcs_press():
    ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-reforecasts-pressure',
                          date="2017-12-28",
                          parameter="z",
                          level=500)
    xds = ds.to_xarray()
    obs = ds.get_observations_as_xarray()
    print(xds)
    print(obs)
    assert xds.z.shape[1:] == obs.z.shape[1:]


if __name__ == "__main__":
    # test_rfcs_surf()
    test_rfcs_press()
