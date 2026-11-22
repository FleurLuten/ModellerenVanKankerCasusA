# Deze moet dus dat excel inlezen en muizen opslaan

import pandas as pd

def load_tumor_data(filename="Data/tumorgrowth.xlsx"):
    """
    Lees de tumorgroeigegevens uit Excel

    Geeft per behandelgroep en per muis de meetdagen
    en bijbehorende tumorvolumes terug
    """

    data = pd.read_excel(filename, header=[0, 2])
    tumor_data = {}
    previous_group = None

    for column_index in range(1, len(data.columns)):
        group = data.columns[column_index][0]
        mouse = data.columns[column_index][1]

        if pd.isna(group):
            group = previous_group
        else:
            previous_group = group

        mouse = str(int(mouse))

        if group not in tumor_data:
            tumor_data[group] = {}
        times = []
        volumes = []

        for row_index in range(len(data)):
            day = data.iloc[row_index, 0]
            volume = data.iloc[row_index, column_index]

            if pd.isna(day) or pd.isna(volume):
                continue
            times.append(float(day))
            volumes.append(float(volume))
        tumor_data[group][mouse] = {
            "times": times,
            "volumes": volumes}

    return tumor_data