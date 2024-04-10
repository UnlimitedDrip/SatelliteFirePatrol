import numpy as np
import geojson
import h5py
import time
import json
from global_land_mask import globe

with h5py.File(f"Data/ECOSTRESS_L2_CLOUD_32186_001_20240310T061757_0601_01 (1).h5", "r") as file:
    # Load bounding coordinates
    print(file)


    print(file["SDS"]["CloudMask"])


# If you want to see the structure in more detail, including groups and datasets within groups
    # def print_structure(name, obj):
    #     print(name, type(obj))
    # file.visititems(print_structure)
