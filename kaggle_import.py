def index_list(find_list, large_list, num):
    for i in range(len(large_list)):
        if find_list[:num] == large_list[i][:num]:
            return i
    return None


def my_int(string):
    if string == '' or string is None:
        return None
    elif string.find(".") != -1:
        return float(string)
    else:
        return int(string)


country = []
country_data = []
suicide_data = []

file = open("master.csv")
for row in file:
    if row[:3] == 'п»ї':
        continue
    s = row.index('"')
    e = row.index('"', s + 1)
    line = (row[:s] + row[s + 1:e].replace(",", "") + row[e + 1:]).split(",")

    data = line[0]
    if data not in country:
        country.append(data)

    data = [country.index(line[0]), my_int(line[1]), my_int(line[8]),  my_int(line[9])]
    if data not in country_data and data[0] == 95:  # if data not in country_data:
        country_data.append(data)

    data = [country.index(line[0]), my_int(line[1]), 0 if line[2] == "male" else 1, my_int(line[4]), my_int(line[5])]
    index = index_list(data, suicide_data, 3)
    if data[0] != 95:    #
        pass             #
    elif index is None:  # if index is None:
        suicide_data.append(data)
    else:
        try:
            suicide_data[index][3] += data[3]
        except TypeError:
            pass
        try:
            suicide_data[index][4] += data[4]
        except TypeError:
            pass
file.close()

# create kaggle_import.sql file for tables country, country_data, suicide_data
# text = "insert into country (id_country, name_country)\n" \
#        "values\n"
# for i in range(len(country)):
#     text += f"({i}, '{country[i]}')" + ("," if i != len(country)-1 else ";") + "\n"
#
# text += "insert into Country_data (id_country, year, hdi, gdp)\n" \
#         "values\n"
#
# for i in range(len(country_data)):
#     text += f"({str(country_data[i])[1:-1]})".replace("None", "Null") + ("," if i != len(country_data)-1 else ";") + "\n"
#
# text += "insert into Suicide_data (id_country, year, sex, suicide, population)\n" \
#         "values\n"
#
# for i in range(len(suicide_data)):
#     text += f"({str(suicide_data[i])[1:-1]})".replace("None", "Null") + ("," if i != len(suicide_data)-1 else ";") + "\n"
#
# file = open("kaggle_import.sql", "w+")
# file.write(text)
# file.close()
