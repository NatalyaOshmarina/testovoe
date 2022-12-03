import pandas as pd
import numpy as np
import datetime

df1 = pd.read_csv('dataset_1.csv', sep=',')
df2 = pd.read_csv('dataset_2.csv', sep=',')
df2.info()

# в датасете с заказами некорректно заполнен столбец с датой - дата заполнена в первой строке,
# далее, в течение дня - пустые значения.
# заполним пустые поля (укажем дату из строки, открывающей день)

df1.fillna('-', inplace=True)

def add_days(arr, dates) -> str:
    for key, value in dates.items():
        if arr >= value[0] and arr < value[1]:
            return key

id_Date = list(df1[df1['Date'] != '-'].index)
value_Date = list(df1['Date'].unique())
value_Date.remove('-')
id_Date.append(len(df1))
list_id = [id_Date[i:i+2] for i in range(len(id_Date))]
dates = dict(zip(value_Date, list_id))
df1['index'] = df1.index
df1.info()

df1['Date'] = df1['index'].apply(add_days, args=(dates, ))

# ответ на вопрос2: В какой из дней было зафиксировано самое большое количество пользователей,
# воспользовавшихся услугами UBER

df = df1.groupby('Date').agg('sum').reset_index()
print(df[['Date', 'Completed Trips ']].sort_values('Completed Trips ', ascending=False).head(1))

# ответ на вопрос3: Какое самое большое количество пользователей, воспользовавшихся услугами UBER,
# было зафиксировано за сутки

print(df['Completed Trips '].sort_values().tail(1))

# ответ на вопрос4: В какой час дня было зафиксировано максимальное количество заказов UBER

df = df1.groupby('Time (Local)').agg('sum').reset_index().tail(1)
print(df['Time (Local)'])

# ответ на вопрос5: какой процент пользователей, не сделавших заказ, составляет среди пользователей,
# зашедших на сайт в выходные (после 17:00 пятницы и до 3:00 воскресенья)
# для решения необходимо преобразовать дату во временной формат

df1.Date = df1.Date.str.replace('Sep', '09')
df1.Date = df1.Date.str.replace('-', '/')
df1.Date = df1.Date.apply(lambda x: str(x[:6] + '2012'))

df1.Date = pd.to_datetime(df1.Date, format='%d/%m/%Y')
df1['Day_of_week'] = df1['Date'].dt.day_name()
df1['weekend'] = np.where(((df1.Day_of_week == 'Friday') & (df1['Time (Local)'] >= 17)) |
                          (df1.Day_of_week == 'Saturday') |
                          ((df1.Day_of_week == 'Sunday') & (df1['Time (Local)'] <= 3)), True, False)
df = df1.groupby('weekend').agg({'Zeroes ': 'sum'})
df.loc['Total'] = df.sum()
res = round(df.iloc[1, 0] / df.iloc[2, 0], 4) * 100
print('Процент нулевых заказов в выходные: {}%'.format(res))

# ответ на вопрос 6: найти средневзвешшеное значение поездок в час за период

df1.loc['Total'] = df1.sum()
res = df1.iloc[336, 4] / 24 / 15
print('Средневзвешенное значение поездок в час за период: {}'.format(res))

# вопрос 7: какая самая загруженная смена? Предполагается, что смены чередуется каждый день.
# Длительность смены - 8 часов

df1['driver'] = '-'
def add_driver(arr, num, driver) -> str:
    if arr['index'] % num == 0 and arr['index'] >= arr[index] - 8:
        return driver
    else:
        return arr.driver

df1['index'] = df1['index'].apply(lambda x: x + 1)
df1['driver'] = df1.apply(add_driver, axis=1, args=(8, '1 driver'))
df1['driver'] = df1.apply(add_driver, axis=1, args=(16, '2 driver'))
df1['driver'] = df1.apply(add_driver, axis=1, args=(24, '3 driver'))
df1['driver'] = df1.apply(add_driver, axis=1, args=(32, '4 driver'))







