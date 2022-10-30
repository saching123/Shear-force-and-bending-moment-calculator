import numpy as np
import VMFunctions as vm

beam_span, load_cases = vm.get_input()

load_set = []  # list of lists containing the load case type, magnitude of the load and
# location of the load

print("Enter 'CF' for point loads (concentrated force), 'UDL' for uniformly distributed loads, \
'PM' for pure moment and 'UVL' for uniformly varying loads.")

for i in range(load_cases):
    load_case_type = str(input("Enter the type for load case " + str(i + 1) + ": "))
    if load_case_type == 'CF':
        load_set.append(vm.get_load_cases_data('CF'))
    elif load_case_type == 'UDL':
        load_set.append(vm.get_load_cases_data('UDL'))
    elif load_case_type == 'UVL':
        load_set.append(vm.get_load_cases_data('UVL'))
    elif load_case_type == 'CL':
        load_set.append(vm.get_load_cases_data('CL'))
    elif load_case_type == 'PM':
        load_set.append(vm.get_load_cases_data('PM'))
    else:
        print("Enter the correct symbols for the desired load cases as mentioned above")

# Statics - calculate reactions forces at supports using input data
# Considers equilibrium of moments with respect to left support
left_reaction, right_reaction = vm.calculate_reactions(beam_span, load_set)

load_set.insert(0, ['R', round(left_reaction, 2), 0, 0, 0])
load_set.append(['R', round(right_reaction, 2), beam_span, 0, 0])

# Shear forces calculation
sum_of_forces = np.zeros(5)
shear_forces_list = []
span_values_list = []

for i in range(len(load_set) - 1):
    if load_set[i][0] == 'R':
        vm.calculate_shear_force_point_load(load_set, i, sum_of_forces, shear_forces_list, span_values_list)

    if load_set[i][0] == 'CF':
        vm.calculate_shear_force_point_load(load_set, i, sum_of_forces, shear_forces_list, span_values_list)

    if load_set[i][0] == 'UDL':
        vm.calculate_shear_force_UDL(load_set, i, sum_of_forces, shear_forces_list, span_values_list)

    elif load_set[i][0] == 'UVL':
        vm.calculate_shear_force_UVL(load_set, i, sum_of_forces, shear_forces_list, span_values_list)

    elif load_set[i][0] == 'CL':
        vm.calculate_shear_force_CL(load_set, i, sum_of_forces, shear_forces_list, span_values_list)

    elif load_set[i][0] == 'PM':
        vm.calculate_shear_force_pure_moment(load_set, i, sum_of_forces, shear_forces_list, span_values_list)


# Plot shear force vs beam span
vm.plot_shear_force_diagram(beam_span, span_values_list, shear_forces_list)

# Bending moments calculation
bending_moments_list = []
x_values_list = []

for i in range(len(load_set) - 1):
    if load_set[i][0] == 'R':
        vm.calculate_bending_moment_point_load(load_set, i, bending_moments_list, x_values_list)

    if load_set[i][0] == 'CF':
        vm.calculate_bending_moment_point_load(load_set, i, bending_moments_list, x_values_list)

    elif load_set[i][0] == 'UDL':
        vm.calculate_bending_moment_UDL(load_set, i, bending_moments_list, x_values_list)

    elif load_set[i][0] == 'UVL':
        vm.calculate_bending_moment_UVL(load_set, i, bending_moments_list, x_values_list)

    elif load_set[i][0] == 'PM':
        vm.calculate_bending_moment_pure_moment(load_set, i, bending_moments_list, x_values_list)

absolute_shear_forces_list = [abs(ele) for ele in shear_forces_list]
max_shear_force = max(absolute_shear_forces_list)

absolute_bending_moments_list = [abs(ele) for ele in bending_moments_list]
max_bending_moment = max(absolute_bending_moments_list)

print("Maximum shear force = ", round(max_shear_force,2), "N")
print("Maximum bending moment = ", round(max_bending_moment,2), "N-m")

print("Reaction at left support = ", round(left_reaction,2), "N")
print("Reaction at right support = ", round(right_reaction,2), "N")

# Plot bending moment vs beam span
vm.plot_bending_moment_diagram(beam_span, x_values_list, bending_moments_list)




