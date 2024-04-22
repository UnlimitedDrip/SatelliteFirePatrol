import h5py
import numpy as np


def check_quality(qc_flags):
    # Check bits 1&0 for quality assurance
    lst_accuracy_bits = np.bitwise_and(qc_flags, 0xC000) >> 14
    if lst_accuracy_bits != 0:
        return True

    return False

def checkUh(bit0P, bit1P, bit14P, bit15P, i, j):
    bit0 = bit0P[i][j]
    bit1 = bit1P[i][j]
    bit14 = bit14P[i][j]
    bit15 = bit15P[i][j]

    return (((bit0 == 0) and (bit1 == 0) and (bit14 == 1) and (bit15 == 1)) or ((bit0 == 0) and (bit1 == 0) and (bit14 == 0) and (bit15 == 1)))

def print_hdf5_file_structure(file_name, cloudMaskFileName):
    with h5py.File(file_name, 'r') as f:
        for key in f.keys():
            print(key)

        print(f["SDS"]["LST"])
        print(f["SDS"]["QC"])
        lst = f["SDS"]["LST"][:]
        qc = f["SDS"]["QC"][:]
        bit0 = np.bitwise_and(qc, 1)
        bit1 = np.bitwise_and(qc, 2)
        bit14 = np.bitwise_and(qc, 2**14) >> 14
        bit15 = np.bitwise_and(qc, 2**15) >> 15

        with h5py.File(f"{cloudMaskFileName}", "r") as file:
            cloudMask = file["SDS"]["CloudMask"][:]
            bit0CloudMask = np.bitwise_and(cloudMask, 1)
            # bit1CloudMask = np.bitwise_and(cloudMask, 2)
            bit1CloudMask = np.bitwise_and(cloudMask, 2) >> 1

        # for row in qcDataBit0:
        #     for col in row:
        #         print(col, end="")
        #     print()

        for rowIndex in range( len(bit0) ):
            for colIndex in range( len(bit0[rowIndex]) ):
                qc_description = check_quality(qc[rowIndex][colIndex])
                # if (bit0CloudMask[rowIndex][colIndex] == 1 and bit1CloudMask[rowIndex][colIndex] == 1 and qc_description):
                # if (bit0CloudMask[rowIndex][colIndex] == 1 and bit1CloudMask[rowIndex][colIndex] == 1 and checkUh(bit0, bit1, bit14, bit15, rowIndex,colIndex) ):
                if (checkUh(bit0, bit1, bit14, bit15, rowIndex,colIndex) ):
                    temp = (lst[rowIndex][colIndex] * .02)
                    temp = (temp - 273.15) * (9/5) + 32

                    if temp > 0:
                        print(temp)
                    else:
                        print("Kill me please")
                # print(temp)

# Usage
file_name = "Data/ECOSTRESS_L2_LSTE_32613_003_20240406T191302_0601_01.h5"  # Replace with your HDF5 file name
cloudFile = "Data/ECOSTRESS_L2_CLOUD_32613_003_20240406T191302_0601_01.h5"

print_hdf5_file_structure(file_name, cloudFile)
