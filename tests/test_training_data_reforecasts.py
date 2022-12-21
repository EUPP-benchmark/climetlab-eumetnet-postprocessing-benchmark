#!/usr/bin/env python3

import climetlab as cml
import numpy as np


# Time and resource consuming - uncomment only if needed
# def test_rfcs_surf():
#     ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface',
#                           date="2017-12-28",
#                           parameter="2t")
#     xds = ds.to_xarray()
#     obs = ds.get_observations_as_xarray()
#     assert xds.t2m.shape[1:] == obs.t2m.shape[1:]
#     assert np.all(xds.time == obs.time)
#     assert np.all(xds.valid_time == obs.valid_time)
#
#
# def test_rfcs_press():
#     ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-pressure',
#                           date="2017-12-28",
#                           parameter="z",
#                           level=500)
#     xds = ds.to_xarray()
#     obs = ds.get_observations_as_xarray()
#     assert xds.z.shape[1:] == obs.z.shape[1:]
#     assert np.all(xds.time == obs.time)
#     assert np.all(xds.valid_time == obs.valid_time)


# def test_rfcs_surf_pp():
#     ds = cml.load_dataset('eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface-processed',
#                           date="2017-12-28",
#                           parameter="mx2t6")
#     xds = ds.to_xarray()
#     obs = ds.get_observations_as_xarray()
#     assert xds.mx2t6.shape[1:] == obs.mx2t6.shape[1:]
#     assert np.all(xds.time == obs.time)
#     assert np.all(xds.valid_time == obs.valid_time)

if __name__ == "__main__":
    # test_rfcs_surf()
    # test_rfcs_press()
    # test_rfcs_surf_pp()
    pass
