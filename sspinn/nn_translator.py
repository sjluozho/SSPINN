import re


def nn_translator(filename, train=False):
    max_el = 10
    max_spec = 3338
    max_cm = 432

    if not isinstance(train, bool):
        raise TypeError

    if not isinstance(filename, str):
        raise TypeError

    file_object = open(filename, 'r')
    line1 = file_object.readline()

    if not line1.lower().startswith('empirical formula:'):
        raise ValueError

    line1 = line1.replace('empirical formula: ', '')
    line1 = line1.replace('Empirical formula: ', '')

    empirical_formula = {}

    matches = re.findall("(\D+)(\d*)", line1)

    for match in matches:
        atom = match[0][0:2]
        if match[1] == '':
            atom_count = 1
        else:
            atom_count = int(match[1])

        if atom in empirical_formula:
            empirical_formula[atom] += atom_count
        else:
            empirical_formula[atom] = atom_count

    el = [0]*max_el

    for key, val in empirical_formula.items():
        if key == 'H':
            el[0] = val
        elif key == 'C':
            el[1] = val
        elif key == 'N':
            el[2] = val
        elif key == 'O':
            el[3] = val
        elif key == 'F':
            el[4] = val
        elif key == 'Cl':
            el[5] = val
        elif key == 'Br':
            el[6] = val
        elif key == 'I':
            el[7] = val
        elif key == 'P':
            el[8] = val
        elif key == 'B':
            el[9] = val

    line2 = file_object.readline()

    if not line2.startswith('peakLocation peakArea peakMultiplicity'):
        raise ValueError

    spectra = [0.0]*max_spec

    line = file_object.readline()

    while not line.startswith('Connectivity Matrix'):
        matches = re.findall("(\d+\.\d)( )(\d+)( )(\D)", line)
        for match in matches:
            if match[4].lower() == 's':
                spectra[int(float(match[0])*10)] = 1.0
            elif match[4].lower() == 'd':
                spectra[int(float(match[0])*10)] = 2.0
            elif match[4].lower() == 't':
                spectra[int(float(match[0])*10)] = 3.0
            elif match[4].lower() == 'q':
                spectra[int(float(match[0])*10)] = 4.0
        line = file_object.readline()

        if line == '':
            break

    if not train:
        connectivity_matrix = None
    else:
        if not line.startswith('Connectivity Matrix'):
            raise ValueError
        connectivity_matrix = [[0.0]*max_cm]*max_cm
        line = file_object.readline()
        atoms = re.findall("([A-Za-z]+)", line)

        offset_dict_i = {'H': 0, 'C': 183, 'N': 327, 'O': 346, 'S': 385,
                         'F': 393, 'Cl': 405, 'Br': 415, 'P': 421, 'I': 423,
                         'B': 429}

        for i in range(0, len(atoms)):
            line = file_object.readline()

            matches = re.findall("(\d)", line)
            cm_row = [0.0]*max_cm

            atom_i = atoms[i]
            offset_i = offset_dict_i[atom_i]

            offset_dict_j = {'H': 0, 'C': 183, 'N': 327, 'O': 346, 'S': 385,
                             'F': 393, 'Cl': 405, 'Br': 415, 'P': 421,
                             'I': 423, 'B': 429}

            for j in range(0, len(atoms)):
                num = int(matches[j])
                atom_j = atoms[j]
                offset_j = offset_dict_j[atom_j]

                if num > 0:
                    cm_row[offset_j] = num

                offset_dict_j[atom_j] += 1

            connectivity_matrix[offset_i] = cm_row
            offset_dict_i[atom_i] += 1

    output = (el + spectra, connectivity_matrix)

    return output
