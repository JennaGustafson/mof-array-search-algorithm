#!/usr/bin/env python
import sys

import numpy as np
from datetime import datetime
print(datetime.now().strftime("%Y_%m_%d__%H_%M_%S"))
from search_algorithm import (read_output_data,
                             yaml_loader,
                             write_output_data,
                             import_experimental_results,
                             import_simulated_data,
                             calculate_pmf,
                             create_bins,
                             bin_compositions,
                             array_pmf,
                             information_gain,
                             choose_best_arrays)

all_results_import = read_output_data(sys.argv[1])
experimental_mass_import = read_output_data(sys.argv[2])

filepath = 'process_config.yaml'
data = yaml_loader(filepath)

mof_array = data['mof_array']
mof_densities_import = {}
mof_experimental_mass = {}

for mof in mof_array:
    mof_densities_import.copy()
    mof_densities_import.update({ mof : data['mofs'][mof]['density']})

num_mixtures = data['num_mixtures']
stdev = data['stdev']
mrange = data['mrange']
gases = data['gases']
number_mofs = data['number_mofs']
number_bins = data['number_bins']

experimental_mass_results, experimental_mass_mofs, experimental_mofs = import_experimental_results(mof_array, experimental_mass_import, mof_densities_import, gases)
import_data_results = import_simulated_data(experimental_mofs, all_results_import, mof_densities_import, gases)
calculate_pmf_results = calculate_pmf(experimental_mass_results, import_data_results, experimental_mofs, stdev, mrange)
create_bins_results = create_bins(experimental_mofs, calculate_pmf_results, gases, number_bins)

num_divisions = 2
while array_size >= number_mofs:
    new_mofs = []
    print(array_size)
    array_pmf_results, list_of_arrays = array_pmf(gases, array_size, experimental_mofs, calculate_pmf_results)
    bin_compositions_results = bin_compositions(gases, list_of_arrays, create_bins_results, array_pmf_results)
    kl_divergence = information_gain(gases, list_of_arrays, bin_compositions_results, create_bins_results)
    all_arrays_ranked = choose_best_arrays(gases, number_mofs, kl_divergence)[0:1]
    for each_mof in all_arrays_ranked:
        new_mofs.extend(list(each_mof['mof array']))
    experimental_mofs = list(np.unique(new_mofs))
    array_size -= 2

print(all_arrays_ranked)
print(datetime.now().strftime("%Y_%m_%d__%H_%M_%S"))
