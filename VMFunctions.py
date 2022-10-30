import numpy as np
import matplotlib.pyplot as plt


def get_input():
    beam_span = float(input(f"Enter the length of the simply supported beam in m: "))
    load_cases = int(input("Enter the total number of external loads acting on the beam: "))
    return beam_span, load_cases


def get_load_cases_data(load_case):
    if load_case == 'CF':
        magnitude = float(input("Enter the magnitude of the concentrated force in N (+ve force upwards, "
                                "-ve downwards): "))
        point_of_action = float(
            input("Enter the horizontal distance in m of the force from the left end of the beam: "))
        return list([load_case, magnitude, point_of_action, 0, 0])

    if load_case == 'UDL':
        magnitude = float(input("Enter the magnitude of the uniformly distributed load\
        in N/m (+ve distribution upwards, -ve downwards): "))
        udl_start = float(input("Enter the horizontal distance in m to the start of UDL\
        from the left end of the beam: "))
        udl_end = float(input("Enter the horizontal distance in m to the end of UDL from\
        the left end of the beam: "))
        return list([load_case, magnitude, udl_start, udl_end, 0])

    if load_case == 'UVL':
        magnitude = float(input("Enter the magnitude of the uniformly varying load in N/m \
        (+ve distribution upwards, -ve downwards): "))
        uvl_start = float(input("Enter the horizontal distance in m to the start of UVL \
        from the left end of the beam: "))
        uvl_End = float(input("Enter the horizontal distance in m to the end of UVL from \
        the left end of the beam: "))
        return list([load_case, magnitude, uvl_start, uvl_End, 0])

    if load_case == 'PM':
        magnitude = float(input("Enter the magnitude of the pure moment in Nm \
        (+ve moment anticlockwise, -ve moment clockwise): "))
        point_of_action = float(
            input("Enter the horizontal distance in m of the moment from the left end of the beam: "))
        return list([load_case, magnitude, point_of_action, 0, 0])

    if load_case == 'CL':
        start_magnitude = float(input("Enter the magnitude at the start of combined loading\
        in N (+ve distribution upwards, -ve downwards): "))
        cl_start = float(input("Enter the horizontal distance in m to the start of CL from \
        the left end of the beam: "))
        end_magnitude = float(input("Enter the magnitude at the end of combined loading in N\
        (+ve distribution upwards, -ve downwards): "))
        cl_end = float(input("Enter the horizontal distance in m to the end of CL from the left\
        end of the beam: "))
        return list([load_case, start_magnitude, cl_start, end_magnitude, cl_end])


# Statics - calculate reactions
def calculate_reactions(beam_span, load_set):
    sum_of_forces = 0
    sum_of_moments = 0

    for e in load_set:
        if e[0] == 'CF':
            sum_of_forces += e[1]
            sum_of_moments += (e[1] * e[2])

        elif e[0] == 'UDL':
            udl_span = e[3] - e[2]
            udl_load = e[1] * udl_span
            sum_of_forces += udl_load
            moment_arm_udl = (e[2] + e[3]) / 2
            sum_of_moments += udl_load * moment_arm_udl

        elif e[0] == 'UVL':
            uvl_span = e[3] - e[2]
            uvl_load = 0.5 * (e[1] * uvl_span)
            sum_of_forces += uvl_load
            moment_arm_uvl = (e[2] + ((2 / 3) * uvl_span))
            sum_of_moments += uvl_load * moment_arm_uvl

        elif e[0] == 'CL':
            udl_span = e[4] - e[2]
            udl_load = e[1] * udl_span
            uvl_load = 0.5 * udl_span * (e[3] - e[1])  # udl_span = uvl_span
            sum_of_forces += udl_load + uvl_load
            moment_arm_udl = (e[2] + e[4]) / 2
            udl_moment = udl_load * moment_arm_udl
            moment_arm_uvl = e[2] + ((2 / 3) * udl_span)
            uvl_moment = uvl_load * moment_arm_uvl
            sum_of_moments += udl_moment + uvl_moment

        elif e[0] == 'PM':
            sum_of_moments += e[1]

    right_reaction = -1 * (sum_of_moments / beam_span)  # summation of Moments = 0
    left_reaction = -1 * (sum_of_forces + right_reaction)  # summation of vertical forces = 0

    return left_reaction, right_reaction


# Shear force calculations
def calculate_shear_force_point_load(load_set, i, sum_of_forces, shear_forces_list, span_values_list):
    x = np.linspace(load_set[i][2], load_set[i + 1][2], 5, endpoint=True)
    sum_of_forces += load_set[i][1]
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x)


def calculate_shear_force_UDL(load_set, i, sum_of_forces, shear_forces_list, span_values_list):
    x = np.linspace(load_set[i][2], load_set[i][3], 5, endpoint=True)
    base = x - load_set[i][2]
    udl_load = load_set[i][1] * base
    sum_of_forces += udl_load
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x)

    x1 = np.linspace(load_set[i][3], load_set[i + 1][2], 5, endpoint=True)
    # sum_of_forces = sum_of_forces[-1] * np.ones(5)
    sum_of_forces[0:-1] = sum_of_forces[-1]
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x1)


def calculate_shear_force_UVL(load_set, i, sum_of_forces, shear_forces_list, span_values_list):
    x = np.linspace(load_set[i][2], load_set[i][3], 5, endpoint=True)
    base = x - load_set[i][2]
    uvl_span = load_set[i][3] - load_set[i][2]
    height = (base / uvl_span) * load_set[i][1]
    uvl_load = 0.5 * base * height
    sum_of_forces += uvl_load
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x)

    x1 = np.linspace(load_set[i][3], load_set[i + 1][2], 5, endpoint=True)
    sum_of_forces[0:-1] = sum_of_forces[-1]
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x1)


# To be checked
def calculate_shear_force_CL(load_set, i, sum_of_forces, shear_forces_list, span_values_list):
    x = np.linspace(load_set[i][2], load_set[i][4], 1000, endpoint=True)
    base = x - load_set[i][2]
    udl_load = load_set[i][1] * base
    uvl_span = load_set[i][4] - load_set[i][2]
    uvlHeight = load_set[i][3] - load_set[i][1]
    height = (base / uvl_span) * uvlHeight
    uvl_load = 0.5 * base * height
    sum_of_forces += udl_load + uvl_load
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x)

    x1 = np.linspace(load_set[i][4], load_set[i + 1][2], 1000, endpoint=True)
    sum_of_forces = sum_of_forces[-1] * np.ones(1000)
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x1)


def calculate_shear_force_pure_moment(load_set, i, sum_of_forces, shear_forces_list, span_values_list):
    x = np.linspace(load_set[i][2], load_set[i + 1][2], 5, endpoint=True)
    shear_forces_list.extend(sum_of_forces)
    span_values_list.extend(x)


def plot_shear_force_diagram(beam_span, span_values_list, shear_forces_list):
    plt.figure(figsize=(10, 6))
    plt.plot(span_values_list, shear_forces_list, 'r', lw=3, linestyle='-')
    plt.fill_between(span_values_list, y1=0, y2=shear_forces_list, color='y', alpha=0.25)
    plt.xlabel("Span (m)", fontsize=15, fontweight="bold")
    plt.ylabel("Shear force (N)", fontsize=20, fontweight="bold")
    plt.title("Shear force diagram", fontsize=20, fontweight="bold")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.axis([0, beam_span, min(shear_forces_list) - 5e3, max(shear_forces_list) + 5e3])
    plt.show()


# Bending moment calculations
def calculate_bending_moment_point_load(load_set, i, bending_moments_list, x_values_list):
    x = np.linspace(load_set[i][2], load_set[i + 1][2], 5, endpoint=True)
    x_values_list.extend(x)
    sum_of_moments = np.zeros(5)
    for j in range(i + 1):
        if load_set[j][0] == 'UDL':
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x - point_of_action))

        elif load_set[j][0] == 'PM':
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign here

        elif load_set[j][0] == 'UVL':
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            moment_arm = (2 / 3) * (load_set[j][3] - load_set[j][2])
            point_of_action = x - (load_set[j][2] + moment_arm)
            sum_of_moments = sum_of_moments + (load * point_of_action)

        else:  # point load
            sum_of_moments = sum_of_moments + (load_set[j][1] * (x - load_set[j][2]))

    bending_moments_list.extend(sum_of_moments)


def calculate_bending_moment_UDL(load_set, i, bending_moments_list, x_values_list):
    x = np.linspace(load_set[i][2], load_set[i][3], 1000, endpoint=True)
    x_values_list.extend(x)
    sum_of_moments = np.zeros(1000)
    # Moments of all load_cases except this UDL in the span of this UDL
    for j in range(i):
        if load_set[j][0] == 'UDL':
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x - point_of_action))

        elif load_set[j][0] == 'PM':
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign here

        elif load_set[j][0] == 'UVL':
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (2 / 3) * (load_set[j][3] - load_set[j][2])
            moment_arm = x - (load_set[j][2] + point_of_action)
            sum_of_moments = sum_of_moments + (load * moment_arm)

        else:
            sum_of_moments += load_set[j][1] * (x - load_set[j][2])

    # Moment of this UDL in this UDL span
    ud_load = load_set[i][1] * (x - load_set[i][2])
    sum_of_moments = sum_of_moments + (ud_load * (x - ((x + load_set[i][2]) / 2)))

    bending_moments_list.extend(sum_of_moments)

    # Moment of all load_cases including this UDL from end of this UDL span to next load_case
    x1 = np.linspace(load_set[i][3], load_set[i + 1][2], 1000, endpoint=True)
    x_values_list.extend(x1)
    sum_of_moments = np.zeros(1000)
    for j in range(i + 1):
        if (load_set[j][0] == 'UDL'):
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x1 - point_of_action))

        elif load_set[j][0] == 'PM':
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign here

        elif load_set[j][0] == 'UVL':
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (2 / 3) * (load_set[j][3] - load_set[j][2])
            moment_arm = x1 - (load_set[j][2] + point_of_action)
            sum_of_moments = sum_of_moments + (load * moment_arm)

        else:
            sum_of_moments = sum_of_moments + (load_set[j][1] * (x1 - load_set[j][2]))

    bending_moments_list.extend(sum_of_moments)


def calculate_bending_moment_pure_moment(load_set, i, bending_moments_list, x_values_list):
    x = np.linspace(load_set[i][2], load_set[i + 1][2], 5, endpoint=True)
    x_values_list.extend(x)
    sum_of_moments = np.zeros(5)
    for j in range(i + 1):
        if load_set[j][0] == 'UDL':
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x - point_of_action))

        elif load_set[j][0] == 'PM':
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign change here

        elif load_set[j][0] == 'UVL':
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (2 / 3) * (load_set[j][3] - load_set[j][2])
            moment_arm = x - (load_set[j][2] + point_of_action)
            sum_of_moments = sum_of_moments + (load * moment_arm)

        else:
            sum_of_moments += load_set[j][1] * (x - load_set[j][2])

    bending_moments_list.extend(sum_of_moments)


def calculate_bending_moment_UVL(load_set, i, bending_moments_list, x_values_list):
    x = np.linspace(load_set[i][2], load_set[i][3], 100, endpoint=True)
    x_values_list.extend(x)
    sum_of_moments = np.zeros(100)
    # Moments of all load_cases except this UVL in the span of this UVL
    for j in range(i):
        if (load_set[j][0] == 'UVL'):
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            moment_arm = (2 / 3) * (load_set[j][3] - load_set[j][2])
            point_of_action = x - (load_set[j][2] + moment_arm)
            sum_of_moments = sum_of_moments + (load * point_of_action)

        elif load_set[j][0] == 'PM':
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign here

        elif load_set[j][0] == 'UDL':
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x - point_of_action))

        else:
            sum_of_moments += load_set[j][1] * (x - load_set[j][2])

    # Moment of this UVL in this UVL span
    base_of_load = x - load_set[i][2]
    height_of_load = ((x - load_set[i][2]) / (load_set[i][3] - load_set[i][2])) * load_set[i][1]
    uv_load = 0.5 * base_of_load * height_of_load
    moment_arm = x - (load_set[i][2] + ((2 / 3) * base_of_load))
    sum_of_moments = sum_of_moments + (uv_load * moment_arm)

    bending_moments_list.extend(sum_of_moments)

    # Moment of all load_cases including this UVL from end of this UVL span to next load_case
    x1 = np.linspace(load_set[i][3], load_set[i + 1][2], 100, endpoint=True)
    x_values_list.extend(x1)
    sum_of_moments = np.zeros(100)
    for j in range(i + 1):
        if (load_set[j][0] == 'UVL'):
            load = 0.5 * load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (2 / 3) * (load_set[j][3] - load_set[j][2])
            moment_arm = x1 - (load_set[j][2] + point_of_action)
            sum_of_moments = sum_of_moments + (load * moment_arm)

        elif (load_set[j][0] == 'UDL'):
            load = load_set[j][1] * (load_set[j][3] - load_set[j][2])
            point_of_action = (load_set[j][2] + load_set[j][3]) / 2
            sum_of_moments = sum_of_moments + (load * (x1 - point_of_action))

        elif (load_set[j][0] == 'PM'):
            sum_of_moments = sum_of_moments - load_set[j][1]  # note the sign here

        else:
            sum_of_moments += load_set[j][1] * (x1 - load_set[j][2])

    bending_moments_list.extend(sum_of_moments)


def plot_bending_moment_diagram(beam_span, x_values_list, bending_moments_list):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values_list, bending_moments_list, 'r', lw=3, linestyle='-')
    plt.fill_between(x_values_list, y1=0, y2=bending_moments_list, color='g', alpha=0.25)
    plt.xlabel("Span (m)", fontsize=15, fontweight="bold")
    plt.ylabel("Bending moment (N-m)", fontsize=20, fontweight="bold")
    plt.title("Bending moment"
              " diagram", fontsize=20, fontweight="bold")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.axis([0, beam_span, min(bending_moments_list) - 5e3, max(bending_moments_list) + 5e3])
    plt.show()
