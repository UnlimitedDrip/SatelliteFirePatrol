import h5py
import numpy as np


def print_hdf5_file_structure(file_name, cloudMaskFileName):
    with h5py.File(file_name, 'r') as f:
        for key in f.keys():
            print(key)
            
        print(f["SDS"]["LST"])
        print(f["SDS"]["QC"])
        lst = f["SDS"]["LST"][:]
        qc = f["SDS"]["QC"][:]
        qcDataBit0 = np.bitwise_and(qc, 1)
        qcDataBit1 = np.bitwise_and(qc, 2) 
        
        with h5py.File(f"{cloudMaskFileName}", "r") as file:
            cloudMask = file["SDS"]["CloudMask"][:]
            bit0CloudMask = np.bitwise_and(cloudMask, 1)
            # bit1CloudMask = np.bitwise_and(cloudMask, 2)
            bit1CloudMask = np.bitwise_and(cloudMask, 2) >> 1
        
        # for row in qcDataBit0:
        #     for col in row:
        #         print(col, end="")
        #     print()
        
        for rowIndex in range( len(qcDataBit0) ):
            for colIndex in range( len(qcDataBit0[rowIndex]) ):
                
                if (qcDataBit0[rowIndex][colIndex] == 0 and qcDataBit1[rowIndex][colIndex] == 0
                    and bit0CloudMask[rowIndex][colIndex] == 1 and bit1CloudMask[rowIndex][colIndex] == 1 ):
                    temp = (lst[rowIndex][colIndex] * .02)
                    temp = (temp - 273.15) * (9/5) + 32
                    
                    if temp < 10:
                        print("Scream")
                    else:
                        print("good thing")

# Usage
file_name = "Data/ECOSTRESS_L2_LSTE_32613_003_20240406T191302_0601_01.h5"  # Replace with your HDF5 file name
cloudFile = "Data/ECOSTRESS_L2_CLOUD_32613_003_20240406T191302_0601_01.h5"

print_hdf5_file_structure(file_name, cloudFile)
