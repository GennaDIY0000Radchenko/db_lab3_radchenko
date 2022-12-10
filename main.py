import matplotlib.pyplot as plt
import psycopg2

username = 'postgres'
password = '314159265'
host = 'localhost'
port = 5432

database = "lab_2"
conn = psycopg2.connect(user=username, password=password, dbname=database)
cur = conn.cursor()

blue = (5 / 255, 20 / 255, 255 / 255)
pink = (255 / 255, 37 / 255, 209 / 255)
green = (32 / 255, 168 / 255, 72 / 255)
yellow = (241 / 255, 255 / 255, 6 / 255)

# for bar : suicides male/female in country
country = "Ukraine"
view_1 = f"create view death_male_female_year_{country} as " \
         'select suicide_data."year", sex, suicide from suicide_data ' \
         'join country ON country.id_country = suicide_data.id_country ' \
         f"where country.name_country = '{country}'"
# cur.execute(view_1)
query_1 = f"select * from death_male_female_year_{country}"

with conn:
    cur.execute(query_1)
    data = []
    for row in cur:
        data.append(list(row))

year_s = min([i[0] for i in data])
year_e = max([i[0] for i in data])
r = year_e - year_s + 1

year = [year_s + i for i in range(r)]
array_male = [0 for i in range(r)]
array_female = [0 for i in range(r)]

for row in data:
    if row[1] == 0:
        array_male[row[0] - year_s] += int(0 if row[2] is None else row[2])
    else:
        array_female[row[0] - year_s] += int(0 if row[2] is None else row[2])

fig_0, ax_0 = plt.subplots()

ax_0.bar(year, array_male, color=blue, width=0.4, label="Men")
year = [i + 0.4 for i in year]
ax_0.bar(year, array_female, color=pink, width=0.4, label="Women")
ax_0.set_title(f"Suicides in {country}")
ax_0.legend()
plt.savefig("save_png/1.png")

# for pie : suicide male/female in country
country = "Ukraine"
view_2 = f'create view total_death_by_sex_{country} as ' \
         'select sex, sum(suicide) from suicide_data ' \
         'join country ON country.id_country = suicide_data.id_country ' \
         f"where country.name_country = '{country}' " \
         'group by sex'
# cur.execute(view_2)
query_2 = f"select * from total_death_by_sex_{country}"

with conn:
    cur.execute(query_2)
    data = []
    for row in cur:
        data.append(list(row))

fig_1, ax_1 = plt.subplots()

ax_1.pie([data[0][1] if data[0][0] == 0 else data[1][1], data[0][1] if data[0][0] == 1 else data[1][1]],
         labels=["male", "female"], autopct='%1.1f%%', explode=(0.01, 0.01), colors=[blue, pink])
ax_1.set_title(f"Total suicides in {country}")
plt.savefig("save_png/2.png")

# for dependency graph
country = "Ukraine"
view_3 = f'create view dependence_death_male_female_gdp_hdi_{country} as ' \
         'select suicide_data."year", sex, suicide, population, hdi, gdp from suicide_data ' \
         'left join country_data on country_data."year" = suicide_data."year" ' \
         'left join country on country.id_country = suicide_data.id_country ' \
         f"where country.name_country = '{country}'"
# cur.execute(view_3)
query_3 = f"select * from dependence_death_male_female_gdp_hdi_{country}"

with conn:
    cur.execute(query_3)
    data = []
    for row in cur:
        data.append(list(row))

year_s = min([i[0] for i in data])
year_e = max([i[0] for i in data])
r = year_e - year_s + 1

fig_2, ax_2 = plt.subplots()
year, array = [], []
for i in range(len(data)):
    if data[i][1] == 0 and data[i][3] != 0:
        try:
            array.append(data[i][2] / data[i][3])
            year.append(data[i][0])
        except TypeError:
            pass
ax_2.plot(year, array, color=blue, label="Men")

year, array = [], []
for i in range(len(data)):
    if data[i][1] == 1 and data[i][3] != 0:
        try:
            array.append(data[i][2] / data[i][3])
            year.append(data[i][0])
        except TypeError:
            pass
ax_2.plot(year, array, color=pink, label="Women")

year, array = [], []
population = [0 for i in range(len(set([i[0] for i in data])))]
for row in data:
    population[row[0] - year_s] += row[3] if row[3] is not None else 0
for row in data:
    if row[0] not in year and row[5] is not None:
        year.append(row[0])
        array.append(row[5] / population[row[0] - year_s] / 10 ** 7)
ax_2.plot(year, array, color=green, label="GDP per capita / 10^7")

year, array = [], []
for row in data:
    if row[4] is not None:
        year.append(row[0])
        array.append(row[4] / 2000)
ax_2.plot(year, array, color=yellow, label="HDI / 2*10^3")

ax_2.legend()
fig_2.tight_layout()
plt.savefig("save_png/3.png")
plt.show()
