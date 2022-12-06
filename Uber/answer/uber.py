import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv('dataset_1.csv', sep=',')
df2 = pd.read_csv('dataset_2.csv', sep=',')
df2.info()

# вопрос1: содержание датасетов.
# первый датасет - заказы. Колонки датасета.
# Date - день
# Time (local) - час
# Eyeballs - число посетителей приложения
# Zeroes - количество посетителей, не нашедших свободное такси
# Completed Trips - количество посетителей, дождавшихся машину
# Requests - количество посетителей, сделавших заказ
# Unique Drivers - количество зарегестрированных водителей

# второй датасет - водители. Колонки датасета.
# Name - имя водителя
# Trips Completed - количество совершенных поездок
# Accept Rate - процент принятых заказов
# Supply Hours - час выхода на линию
# Rating - рейтинг

# сначала работаем с первым датасетом - заказы
# в датасете с заказами некорректно заполнен столбец с датой - дата заполнена в первой строке,
# далее, в течение дня - пустые значения.
# заполним пустые поля (укажем дату из строки, открывающей день)

df1.fillna('-', inplace=True)


def add_days(arr, dates: dict) -> str:
    for key, value in dates.items():
        if arr >= value[0] and arr < value[1]:
            return key


id_Date = list(df1[df1['Date'] != '-'].index)
value_Date = list(df1['Date'].unique())
value_Date.remove('-')
id_Date.append(len(df1))
list_id = [id_Date[i:i+2] for i in range(len(id_Date))]
dates = dict(zip(value_Date, list_id))
df1['Index'] = df1.index
df1.info()

df1['Date'] = df1['Index'].apply(add_days, args=(dates, ))

# вопрос2: В какой из дней было зафиксировано самое большое количество пользователей,
# воспользовавшихся услугами UBER

df = df1.groupby('Date').agg('sum').reset_index()
print(df[['Date', 'Completed Trips ']].sort_values('Completed Trips ', ascending=False).head(1))

# вопрос3: Какое самое большое количество пользователей, воспользовавшихся услугами UBER,
# было зафиксировано за сутки

print(df['Completed Trips '].sort_values().tail(1))

# вопрос4: В какой час дня было зафиксировано максимальное количество заказов UBER

df = df1.groupby('Time (Local)').agg('sum').reset_index().tail(1)
print(df['Time (Local)'])

# вопрос5: какой процент пользователей, не сделавших заказ, составляет среди пользователей,
# зашедших на сайт в выходные (после 17:00 пятницы и до 3:00 воскресенья)
# для решения необходимо преобразовать дату во временной формат и добавить столбец с днями недели

df1.Date = df1.Date.str.replace('Sep', '09')
df1.Date = df1.Date.str.replace('-', '/')
df1.Date = df1.Date.apply(lambda x: str(x[:6] + '2012'))

df1.Date = pd.to_datetime(df1.Date, format='%d/%m/%Y')
df1['Day_of_week'] = df1['Date'].dt.day_name()
df1['Weekend'] = np.where(((df1.Day_of_week == 'Friday') & (df1['Time (Local)'] >= 17)) |
                          (df1.Day_of_week == 'Saturday') |
                          ((df1.Day_of_week == 'Sunday') & (df1['Time (Local)'] <= 3)), True, False)
df = df1.groupby('Weekend').agg({'Zeroes ': 'sum'})
df.loc['Total'] = df.sum()
res = round(df.iloc[1, 0] / df.iloc[2, 0], 4) * 100
print('Процент нулевых заказов в выходные: {res}% от количества всех заказов'.format(res=res))

# вопрос 6: найти средневзвешшеное значение поездок в час за период

df1.loc['Total'] = df1.sum(numeric_only=True)
res = df1.iloc[336, 4] / 24 / 15
print('Средневзвешенное значение поездок в час за период: {res}'.format(res=res))

# вопрос 7: какая самая загруженная смена? Предполагается, что смены смещаются каждый день.
# Длительность смены - 8 часов
# Поскольку у нас длительность смены составляет 8 часов и смены должны смещаться, общее количество бригад - 4
# (3 смены на сутки + одна смена на сдвиг)
# алгоритм решения: сначала разбиваем период 32 часа на 4 чередующиеся бригады
# затем определяем бригаду с самым высоким значением суммарного показателя 'Completed Trips'

driver1 = list()
driver2 = list()
driver3 = list()
driver4 = list()
for i in range(0, len(df) + 1, 32):
    list1 = [num for num in range(i, i + 8)]
    list2 = [num for num in range(i + 8, i + 16)]
    list3 = [num for num in range(i + 16, i + 24)]
    list4 = [num for num in range(i + 24, i + 32)]
    driver1.extend(list1)
    driver2.extend(list2)
    driver3.extend(list3)
    driver4.extend(list4)
value = [driver1, driver2, driver3, driver4]
key = ['бригада 1', 'бригада 2', 'бригада 3', 'бригада 4']
drivers = dict(zip(key, value))


def add_col(arr, some_dict: dict) -> str:
    for key, value in some_dict.items():
        if arr in value:
            return key


df1['Driver'] = df1['Index'].apply(add_col, args=(drivers, ))
df = df1.groupby('Driver').agg({'Completed Trips ': 'sum'}).reset_index().tail(1)
res = df.iloc[0, 0]
print('Самое большое количество активных поездок за период совершила: {res}'.format(res=res))

# вопрос 8: всегда ли повышение спроса на поездки ведет к повышению поездок. Визулизируйте ответ,
# если это необходимо

df = df1[['Date', 'Eyeballs ', 'Completed Trips ']]
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df['Date'], df['Eyeballs '], label='Потребность')
ax.plot(df['Date'], df['Completed Trips '], label='Поездки')
ax.legend()
plt.show()

# вопрос 9: в какой из 72-часового периода было наибольшее количество не сделавших заказ?

values = [[num for num in range(i, i+72)] for i in range(0, len(df1), 72)]
keys = [value_Date[i][:6] + ' - ' + value_Date[i + 2][:6] for i in range(0, len(value_Date), 3)]
periods = dict(zip(keys, values))

df1['Period'] = df1['Index'].apply(add_col, args=(periods, ))
df = df1.groupby('Period').agg({'Zeroes ': 'sum'}).reset_index().tail(1)
res = df.iloc[0, 0]
print('Самое большое количество пользователей, не сделавших заказ, зафиксировано в период: {res}'.format(res=res))

# вопрос 10: если бы вы могли добавить 5 водителей в один час, в какой бы час вы их добавили?
# предполагается, что на одного водителя приходится 2 пассажира.
# чтобы ответить на вопрос, надо найти час, в котором было максимальное суммарное количество пользователей,
# не нашедших свободное такси (колока Zeroes)

df = df1.groupby('Time (Local)').agg({'Zeroes ': 'sum'}).reset_index().tail(2)
res = df.iloc[0, 0]
print('Максимальное количество пользователей, не нашедших свободное такси, приходится на: {res} час.'.format(res=res))

# вопрос 11: в датасете данные представлены ровно за две недели?

if ((len(df1) - 1) / 24) % 2 == 0:
    print('В датасете представлены данные ровно за две недели.')
else:
    res = (len(df1) - 1) / 24
    print('В датасете представлены данные за {res} дней'.format(res=res))

# вопрос 12: найдите час, соответствующий "концу дня" (спрос и предложение находятся на самом низком уровне)
# визуализируйте ответ, если это необходимо

df = df1.iloc[:-1, :].groupby('Time (Local)').agg({'Completed Trips ': 'sum', 'Eyeballs ': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df['Time (Local)'], df['Eyeballs '], label='Потребность')
ax.plot(df['Time (Local)'], df['Completed Trips '], label='Поездки')
ax.set_xticks(list(range(0, 25)))
ax.legend()
plt.show()

# вопрос 13: Выручка таксиста за день составляет 200$. Такстист работает 6 дней в неделю, три недели в месяц.
# Расходы составляют:
# бензин - 200$ в неделю
# страховка - 400$ в месяц
# аренда автомобиля - 500$ в месяц.
# Сколько заработает такстист за год?

fare = 200 * (365 // 7 / 4 * 3 * 6)
gas = 200 * (365 // 7 / 4 * 3)
fix_costs = (400 + 500) * 12
profit = fare - gas - fix_costs
print('\nПри ежедневной выручке 200$, расходах:\nбензин - 200$ в неделю,\nстраховка - 400$ в месяц,\n'
      'аренда автомобиля - 500$ в месяц,\nи графике работы 6 дней в неделю, три недели в месяц\n'
      'за год работы доход (после вычета всех расходов) составит:\nвыручка за год - расходы на бензин - '
      'постоянные расходы (страховка и аренда автомобиля)\n{res}$ - {gas}$ - {fix}$ = {profit}$'.format(
    res=fare, gas=gas, fix=fix_costs, profit=profit
))

# вопрос 14: насколько необходимо увеличить ежедневную выручку,
# чтобы суметь купить автомобиль стоимостью 40 000$ за год работы

res = round(40000 / (365 // 7) * 4 / 3 / 6, 2)
print('Чтобы накопить на автомобиль стоимостью 40 000$ за год, при доходах и расходах, описанных выше,\n'
      'необходомо ежедневную выручку повысить на {res}$'.format(res=res))

# вопрос 16: какой показатель не будет расти в час-пик?

df = df1.iloc[:-1, :].groupby('Time (Local)').agg({'Completed Trips ': 'sum', 'Eyeballs ': 'sum',
                                                   'Zeroes ': 'sum', 'Requests ': 'sum',
                                                   'Unique Drivers': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df['Time (Local)'], df['Eyeballs '], label='Зашли в приложение')
ax.plot(df['Time (Local)'], df['Completed Trips '], label='Совершили поездку')
ax.plot(df['Time (Local)'], df['Zeroes '], label='Не сделали заказ')
ax.plot(df['Time (Local)'], df['Requests '], label='Выбрали другое такси')
ax.plot(df['Time (Local)'], df['Unique Drivers'], label='Количество водителей')
ax.set_xticks(list(range(0, 25)))
ax.legend()
plt.show()

# далее работаем с датасетом водителей.
# В этом датасете содержится информация о водителях, попавших в маркетинговую акцию.
# Водителям были выделены два опциона

# первый опцион - 50$ каждому водители, вышедшему на линию до 8 часов, взявшему не менее 90%
# от предложенных заказов, выполневшему не менее 10 поездок и имеющему рейтинг не менее 4,7

# второй опцион, - 4$ за поездку, - всем водителям, выполнивим не менее 12 заказов с рейтингом не ниже 4,7

# вопрос 25: какое суммарное значение опциона 1?
# сначала данные в колонке 'Accept Rate' переведем в числовое значение
df2['Accept Rate'] = df2['Accept Rate'].str.replace('%', '').astype(int)
res = len(df2[(df2['Trips Completed'] >= 10) & (df2['Accept Rate'] >= 90)
          & (df2['Rating'] >= 4.7) & (df2['Supply Hours'] < 8)]) * 50
print('Сумамрное значение опциона 1 составило: {res}$'.format(res=res))

# вопрос 26: какое суммарное значение опциона 2?
res = df2[(df2['Trips Completed'] >= 12) & (df2['Rating'] >= 4.7)]['Trips Completed'].sum() * 4
print('Сумамрное значение опциона 2 составило: {res}$'.format(res=res))

# вопрос 27: как много водителей получило опцион 1, но не получило опцион 2?
res = len(df2[(df2['Trips Completed'] >= 10) & (df2['Accept Rate'] >= 90)
          & (df2['Rating'] >= 4.7) & (df2['Supply Hours'] < 8)]) - len(
    df2[(df2['Trips Completed'] >= 12) & (df2['Accept Rate'] >= 90)
          & (df2['Rating'] >= 4.7) & (df2['Supply Hours'] < 8)])
print('Получило опцион 1 и не получило опцион 2: {res} водителей'.format(res=res))

# вопрос 28: какой процент водителей, обладающих рейтингом 4,7 и выше, выполнило меньше 10 поездок
# и согласилось на менее 90% предложенных заказов
res = round(len(
    df2[(df2['Trips Completed'] < 10) & (df2['Accept Rate'] < 90) & (df2['Rating'] >= 4.7)]) / len(
    df2) * 100, 2)
print('Процент водителей, выполнивших менее 10 поездок, обладающих рейтингом не ниже 4,7 и\nсогласившихся на'
      'менее чем 90% предложенных заказов составляет {res}% от общего числа водителей'.format(res=res))