import numpy as np
import pandas as pd
from numpy import ndarray
from gzip import GzipFile
from nibabel import FileHolder, Nifti1Image
import streamlit as st

def read_file(byte_file):
    # See https://stackoverflow.com/questions/62579425/simpleitk-read-io-byteio
    fh = FileHolder(fileobj=GzipFile(fileobj=byte_file))
    img = Nifti1Image.from_file_map({'header': fh, 'image': fh})
    arr = np.array(img.dataobj)
    return arr, img.header


def compute_dvh(_dose: np.ndarray, _struct_mask: np.ndarray, max_dose = 65, step_size = 0.1,
    ) -> tuple[ndarray, ndarray]:

    dose_in_oar = _dose[_struct_mask > 0]
    bins = np.arange(0, max_dose, step_size)
    total_voxels = len(dose_in_oar)
    values = []

    if total_voxels == 0:
        # There's no voxels in the mask
        values = np.zeros(len(bins))
    else:
        for bin in bins:
            number = (dose_in_oar >= bin).sum()
            value = (number / total_voxels) * 100
            values.append(value)
        values = np.asarray(values)

    return bins, values


def dvh_from_files(dose_file, mask_files):
    dose_volume, dose_header = read_file(dose_file)

    structure_masks = {}
    struct_identifiers = []
    for mask_file in mask_files:
        mask_volume, mask_header = read_file(mask_file)
        struct_name = mask_file.name.split(".")[0]
        struct_identifiers.append(struct_name)
        structure_masks[struct_name] = mask_volume

    dvh_data = {}
    max_dose = 70
    step_size = 0.1
    dvh_data["Dose"] = np.arange(0, max_dose, step_size)

    for structure in structure_masks.keys():
        bins, values = compute_dvh(dose_volume, structure_masks[structure], max_dose, step_size)
        dvh_data[structure] = values

    df = pd.DataFrame.from_dict(dvh_data)
    df = pd.melt(df, id_vars=['Dose'], value_vars=struct_identifiers, var_name='Structure', value_name='Volume')
    return df
