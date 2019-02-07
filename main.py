import matplotlib.pyplot as plt


# analyze the columns data and return a dictionary of strings
def columns_analyze(data1):
    # creates dictionary for all the data and variables of the axis
    dic = {}
    x_axis = data1[-2]
    # add the x axis to the dictionary and remove it from the data
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data1.remove(x_axis)
    y_axis = data1[-1]
    # add the y axis to the dictionary and remove it from the data
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data1.remove(y_axis)
    # remove the spare line before the axes
    spare_line = data1[-1]
    data1.remove(spare_line)
    # creates list of x,y,dx,dy
    first_line_list = data1[0].lower().strip().split(' ')
    data1.remove(data1[0])
    # creates empty list for each column
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    # add columns to lists and check if there is length error
    try:
        for line in data1:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
        # add the columns to the corresponding dictionary key
    dic[first_line_list[0]] = first_list
    dic[first_line_list[1]] = second_list
    dic[first_line_list[2]] = third_list
    dic[first_line_list[3]] = forth_list
    # check if the uncertainties values dx and dy are positive
    dx_values = dic['dx']
    dy_values = dic['dy']
    for index in range(len(first_list)):
        if float(dx_values[index]) <= 0 or float(dy_values[index]) <= 0:
            return 'Input file error: Not all uncertainties are positive.'
    return dic


# analyze the row data nd return a dictionary of strings
def row_analyze(data1):
    # creates dictionary for all the data and variables of the axis
    dic = {}
    x_axis = data1[-2]
    # add the x axis to the dictionary and remove it from the data
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data1.remove(x_axis)
    y_axis = data1[-1]
    # add the y axis to the dictionary and remove it from the data
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data1.remove(y_axis)
    # remove the spare line before the axes
    spare_line = data1[-1]
    data1.remove(spare_line)
    # set the length of the first line as base to check for errors
    first_line_list = data1[0].strip().split(' ')
    line_length = len(first_line_list)
    # for each line determinate for what variable it belongs, and add to dictionary
    for line in data1:
        fixed_line = line.lower().strip().split(' ')
        # check if the length of the row is equal to the the base line
        if len(fixed_line) != line_length:
            return "Input file error: Data lists are not the same length."
        if fixed_line[0] == 'x':
            dic['x'] = fixed_line[1:]
        if fixed_line[0] == 'dx':
            # check if all values are positive, and if not, add them to the dictionary
            for indx in range(1, len(fixed_line)):
                if float(fixed_line[indx]) < 0:
                    return 'Input file error: Not all uncertainties are positive.'
            dic['dx'] = fixed_line[1:]
        if fixed_line[0] == 'y':
            dic['y'] = fixed_line[1:]
        if fixed_line[0] == 'dy':
            # check if all values are positive, and if not, add them to the
            for indx in range(1, len(fixed_line)):
                if float(fixed_line[indx]) < 0:
                    return 'Input file error: Not all uncertainties are positive.'
            dic['dy'] = fixed_line[1:]
    return dic


def type_determination(data_list):
    first_row = data_list[0].lower().strip().split(' ')
    # determinate if file in rows or columns.
    if first_row[1][0] == 'x' or first_row[1][0] == 'y' or first_row[1][0] == 'd':
        return columns_analyze(data_list)
    else:
        return row_analyze(data_list)


# makes the dictionary values floats for easy calculating and plotting
def dictionary_to_float(original_dic):
    float_dic = {}
    # creates lists of each key of the dictionary
    x_str = original_dic['x']
    y_str = original_dic['y']
    dx_str = original_dic['dx']
    dy_str = original_dic['dy']
    # for each key, append its values in floats
    x_list = []
    for value in x_str:
        x_list.append(float(value))
    float_dic['x'] = x_list
    y_list = []
    for value in y_str:
        y_list.append(float(value))
    float_dic['y'] = y_list
    dx_list = []
    for value in dx_str:
        dx_list.append(float(value))
    float_dic['dx'] = dx_list
    dy_list = []
    for value in dy_str:
        dy_list.append(float(value))
    float_dic['dy'] = dy_list
    # add the axis to the new dictionary
    float_dic['x axis'] = original_dic['x axis']
    float_dic['y axis'] = original_dic['y axis']
    return float_dic


# this function returns the evaluated fitting parameters
def eval_fitting_parameters(float_dict):
    x_values = float_dict['x']
    y_values = float_dict['y']
    dy_values = float_dict['dy']
    n = len(float_dict['x'])  # number of data points (constant)


# this function calculate the average value of argument
    def calculate_avg(values, dys):
        sum_avg = 0
        sum_dys = 0
        for index in range(n):
            temp_value = (values[index])/(dys[index]**2)
            sum_avg += temp_value
            sum_dys += 1/(dys[index]**2)
        avg = sum_avg / sum_dys
        return avg

    # this function calculate the average value of the squared values
    def calculate_sq_avg(values, dys):
        sum_sq = 0
        sum_dys = 0
        for index in range(n):
            temp_value = values[index]
            sq_temp_value = (temp_value ** 2)/(dys[index]**2)
            sum_sq += sq_temp_value
            sum_dys += 1/(dys[index]**2)
        sq_avg = sum_sq / sum_dys
        return sq_avg

    # this function calculate the average value of the product of x and y
    def calculate_xy_avg(values1, values2, dys):
        sum_xy = 0
        sum_dys = 0
        for index in range(n):
            xy = (values1[index] * values2[index])/(dys[index]**2)
            sum_xy += xy
            sum_dys += 1/(dys[index]**2)
        xy_avg = sum_xy / sum_dys
        return xy_avg

    # this function calculate the value of chi^2.
    def calculate_chi_sq(input_dict):
        sum_chi_sq = 0
        for index in range(n):
            yi = input_dict['y'][index]
            xi = input_dict['x'][index]
            dyi = input_dict['dy'][index]
            temp_value = ((yi - (a * xi + b))/dyi)**2
            sum_chi_sq += temp_value
        return sum_chi_sq
    # now calculate the evaluation parameters
    x = calculate_avg(x_values, dy_values)
    y = calculate_avg(y_values, dy_values)
    dy_sq = calculate_sq_avg(dy_values, dy_values)
    x_sq = calculate_sq_avg(x_values, dy_values)
    xy = calculate_xy_avg(x_values, y_values, dy_values)
    x_sq_avg = x ** 2
    a = (xy - x * y)/(x_sq - x_sq_avg)
    da = (dy_sq/(n * (x_sq - x_sq_avg))) ** 0.5
    b = y - a * x
    db = ((dy_sq * x_sq)/(n * (x_sq - x_sq_avg))) ** 0.5
    chi_sq = calculate_chi_sq(float_dict)
    chi_sq_red = chi_sq/(n - 2)
    return [a, da, b, db, chi_sq, chi_sq_red]


# finds the lowest x and the highest x in the data for the plot
def find_x_min_and_max(dic):
    x_min = min(dic['x'])
    x_max = max(dic['x'])
    return [x_min, x_max]


# finds y values that compatible for x_min/x_max in order to plot the linear fit
def calculate_y_min_and_max(x_min_max_list, linear_fit_list):
    a = linear_fit_list[0]
    b = linear_fit_list[2]
    x_min = x_min_max_list[0]
    x_max = x_min_max_list[1]
    y_min = a * x_min + b
    y_max = a * x_max + b
    return [y_min, y_max]


# plot and saves the data
def linear_plot(dic, linear_fit_values):
    x_min_and_max_values = find_x_min_and_max(dic)
    y_min_and_max_values = calculate_y_min_and_max(x_min_and_max_values,
                                                   linear_fit_values)
    x = dic['x']
    y = dic['y']
    dx = dic['dx']
    dy = dic['dy']
    x_axis = dic['x axis']
    y_axis = dic['y axis']
    # plots the error 'cross' for each data point on the plot
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue", barsabove=True)
    # plots the red line from the lowest x value to the highest x value, and their corresponding y values
    plt.plot(x_min_and_max_values, y_min_and_max_values, 'r')
    # add the axis
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')


def fit_linear(filename):
    my_file = open(filename, 'r')
    data = my_file.readlines()
    input_dic = type_determination(data)
    if type(input_dic) == str:
        print(input_dic)
    else:
        floating_dic = dictionary_to_float(input_dic)
        eval_parameters = eval_fitting_parameters(floating_dic)
        linear_plot(floating_dic, eval_parameters)
        print('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.format(
            eval_parameters[0], eval_parameters[1], eval_parameters[2], eval_parameters[3],
            eval_parameters[4], eval_parameters[5]))
    my_file.close()


def analyze_bonus_cols(data1):
    # creates dictionary for all the data and variables of the axis
    dic = {}
    # add the b parameters to the dictionary and remove it from the data
    b_parameters = data1[-1]
    b_parameters_list = b_parameters.lower().strip().split(' ')
    dic[b_parameters_list[0]] = b_parameters_list[1], b_parameters_list[2], b_parameters_list[3]
    data1.remove(b_parameters)
    # add the a parameters to the dictionary and remove it from the data
    a_parameters = data1[-1]
    a_parameters_list = a_parameters.lower().strip().split(' ')
    dic[a_parameters_list[0]] = a_parameters_list[1], a_parameters_list[2], a_parameters_list[3]
    data1.remove(a_parameters)
    # remove the spare line before the axes
    data1 = data1[:-1]
    # add the x axis to the dictionary and remove it from the data
    x_axis = data1[-2]
    # add the x axis to the dictionary and remove it from the data
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data1.remove(x_axis)
    y_axis = data1[-1]
    # add the y axis to the dictionary and remove it from the data
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data1.remove(y_axis)
    # remove the spare line before the axes
    spare_line = data1[-1]
    data1.remove(spare_line)
    # creates list of x,y,dx,dy
    first_line_list = data1[0].lower().strip().split(' ')
    data1.remove(data1[0])
    # creates empty list for each column
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    # add columns to lists and check if there is length error
    try:
        for line in data1:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    # add the columns to the corresponding dictionary key
    dic[first_line_list[0]] = first_list
    dic[first_line_list[1]] = second_list
    dic[first_line_list[2]] = third_list
    dic[first_line_list[3]] = forth_list
    # check if the uncertainties values dx and dy are positive
    dx_values = dic['dx']
    dy_values = dic['dy']
    for indx in range(len(first_list)):
        if float(dx_values[indx]) < 0 or float(dy_values[indx]) < 0:
            return 'Input file error: Not all uncertainties are positive.'
    return dic


def analyze_bonus_rows(data1):
    # creates dictionary for all the data and variables of the axis
    dic = {}
    # add the b parameters to the dictionary and remove it from the data
    b_parameters = data1[-1]
    b_parameters_list = b_parameters.lower().strip().split(' ')
    dic[b_parameters_list[0]] = b_parameters_list[1], b_parameters_list[2], b_parameters_list[3]
    data1.remove(b_parameters)
    # add the a parameters to the dictionary and remove it from the data
    a_parameters = data1[-1]
    a_parameters_list = a_parameters.lower().strip().split(' ')
    dic[a_parameters_list[0]] = a_parameters_list[1], a_parameters_list[2], a_parameters_list[3]
    data1.remove(a_parameters)
    # remove the spare line before the axes
    data1 = data1[:-1]
    # add the x axis to the dictionary and remove it from the data
    x_axis = data1[-2]
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data1.remove(x_axis)
    y_axis = data1[-1]
    # add the y axis to the dictionary and remove it from the data
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data1.remove(y_axis)
    # remove the spare line before the axes
    data1 = data1[:-1]
    # set the length of the first line as base to check for errors
    first_line_list = data1[0].strip().split(' ')
    line_length = len(first_line_list)
    # for each line determinate for what variable it belongs, and add to dictionary
    for line in data1:
        fixed_line = line.lower().strip().split(' ')
        # check if the length of the row is equal to the the base line
        if len(fixed_line) != line_length:
            return "Input file error: Data lists are not the same length."
        if fixed_line[0] == 'x':
            dic['x'] = fixed_line[1:]
        if fixed_line[0] == 'dx':
            # check if all values are positive, and if not, add them to the dictionary
            for index in range(1, len(fixed_line)):
                if float(fixed_line[index]) < 0:
                    return'Input file error: Not all uncertainties are positive.'
            dic['dx'] = fixed_line[1:]
        if fixed_line[0] == 'y':
            dic['y'] = fixed_line[1:]
        if fixed_line[0] == 'dy':
            # check if all values are positive, and if not, add them to the
            for index in range(1, len(fixed_line)):
                if float(fixed_line[index]) < 0:
                    return 'Input file error: Not all uncertainties are positive.'
            dic['dy'] = fixed_line[1:]
    return dic


def bonus_type_determination(data_list):
    first_row = data_list[0].lower().strip().split(' ')
    # determinate if file in rows or columns
    if first_row[1][0] == 'x' or first_row[1][0] == 'y' or first_row[1][0] == 'd':
        return analyze_bonus_cols(data_list)
    else:
        return analyze_bonus_rows(data_list)


# makes the dictionary values floats for easy calculating and plotting
def bonus_dictionary_to_float(original_dic):
    float_dic = {}
    # creates lists of each key of the dictionary
    x_str = original_dic['x']
    y_str = original_dic['y']
    dx_str = original_dic['dx']
    dy_str = original_dic['dy']
    a_str = original_dic['a']
    b_str = original_dic['b']
    # for each key, append its values in floats
    temp_list = []
    for value in x_str:
        temp_list.append(float(value))
    float_dic['x'] = temp_list
    temp_list = []
    for value in y_str:
        temp_list.append(float(value))
    float_dic['y'] = temp_list
    temp_list = []
    for value in dx_str:
        temp_list.append(float(value))
    float_dic['dx'] = temp_list
    temp_list = []
    for value in dy_str:
        temp_list.append(float(value))
    float_dic['dy'] = temp_list
    temp_list = []
    for value in a_str:
        temp_list.append(float(value))
    float_dic['a'] = temp_list
    temp_list = []
    for value in b_str:
        temp_list.append(float(value))
    float_dic['b'] = temp_list
    # add the axis to the new dictionary
    float_dic['x axis'] = original_dic['x axis']
    float_dic['y axis'] = original_dic['y axis']
    return float_dic


# calculates the chi squared from given a and b
def calculate_temp_chi(a, b, float_dict):
    chi_sq = 0
    for index in range(len(float_dict['x'])):
        xi = float_dict['x'][index]
        xiplus = xi + float_dict['dx'][index]
        ximinus = xi - float_dict['dx'][index]
        yi = float_dict['y'][index]
        dyi = float_dict['dy'][index]
        temp = ((yi - (a * xi + b)) / ((dyi ** 2 +
                                        (a * xiplus + b - (a * ximinus + b)) ** 2) ** 0.5))
        chi_sq += (temp ** 2)
    return chi_sq


# this function calculate the value of chi^2 for all the a and b values, then returns
# a list with the minimum chi^2 and its corresponding a and b
def calculate_bonus_chi_sq(float_dict):
    min_a = min((float_dict['a'][0]), (float_dict['a'][1]))
    max_a = max((float_dict['a'][0]), (float_dict['a'][1]))
    step_a = abs(float_dict['a'][2])
    min_b = min((float_dict['b'][0]), (float_dict['b'][1]))
    max_b = max((float_dict['b'][0]), (float_dict['b'][1]))
    step_b = abs(float_dict['b'][2])
    # set up the base for the while loop
    min_chi = calculate_temp_chi(min_a, min_b, float_dict)
    chi_min_a = min_a
    chi_min_b = min_b
    b = min_b
    # for each a and b check if the chi is the lowest
    while b <= max_b:
        a = min_a
        while a <= max_a:
            temp_chi = calculate_temp_chi(a, b, float_dict)
            if temp_chi < min_chi:
                min_chi = temp_chi
                chi_min_a = a
                chi_min_b = b
            a = round(a + step_a, 2)
        b = round(b + step_b, 2)
    return [chi_min_a, step_a, chi_min_b, step_b, min_chi]


# this function makes a list of all the a values and their corresponding chi values
# for a single b values
def parameter_lists(float_dict, min_b):
    min_a = min((float_dict['a'][0]), (float_dict['a'][1]))
    max_a = max((float_dict['a'][0]), (float_dict['a'][1]))
    step_a = abs(float_dict['a'][2])
    chi_values = []
    a_values = []
    a = min_a
    while a <= max_a:
        a_values.append(a)
        corr_chi = calculate_temp_chi(a, min_b, float_dict)
        chi_values.append(corr_chi)
        a += step_a
    return [a_values, chi_values]


# this function plots and saves the graph of chi and a.
def plot_chi(non_linear_points, min_b):
    plt.clf()
    x = non_linear_points[0]
    y = non_linear_points[1]
    plt.plot(x, y)
    plt.xlabel("a")
    mini_b = str(min_b)
    plt.ylabel("chi2(a,b="+mini_b+")")
    plt.savefig('numeric_sampling.svg', bbox_inches="tight")


# this func plots the data
def plot_bonus(float_dic, eval_parameters):
    # finds the highest and lowest x values and their corresponding y values
    x_min_and_max = [min(float_dic['x']), max(float_dic['x'])]
    y_min_and_max = []
    for running_x in x_min_and_max:
        running_y = running_x * eval_parameters[0] + eval_parameters[2]
        y_min_and_max.append(running_y)
    # plots the same as part one of the project
    x = float_dic['x']
    y = float_dic['y']
    dx = float_dic['dx']
    dy = float_dic['dy']
    x_axis = float_dic['x axis']
    y_axis = float_dic['y axis']
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue", barsabove=True)
    plt.plot(x_min_and_max, y_min_and_max, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')


def search_best_parameter(filename):
    bonus_file = open(filename, 'r')
    bonus_data = bonus_file.readlines()
    input_dic = bonus_type_determination(bonus_data)
    if type(input_dic) == str:
        print(input_dic)
    else:
        dic = bonus_dictionary_to_float(input_dic)
        eval_parameters = calculate_bonus_chi_sq(dic)
        chi_sq_red = eval_parameters[4]/((len(dic['x']))-2)
        eval_parameters.append(chi_sq_red)
        print('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.format
              (eval_parameters[0], eval_parameters[1], eval_parameters[2],
               eval_parameters[3], eval_parameters[4], eval_parameters[5]))
        plot_bonus(dic, eval_parameters)
        chi_plot_data = parameter_lists(dic, eval_parameters[2])
        plot_chi(chi_plot_data, eval_parameters[2])
    bonus_file.close()
