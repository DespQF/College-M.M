import pandas as pd

# Загружаем CSV файл
df = pd.read_csv('dom_click.csv')

# Очищаем данные в столбце "location"
df['location'] = df['location'].str.replace(r'^Россия, Московская область,\s*', '', regex=True)

# Удаляем столбцы 'ipoteka_rate' и 'discount' и 'year_of_construction'
df.drop(columns=['ipoteka_rate', 'discount', 'year_of_construction'], inplace=True)

# Преобразование столбцов floor, floor_count и rooms_count в int
df['floor'] = pd.to_numeric(df['floor'], errors='coerce').fillna(0).astype(int)
df['floor_count'] = pd.to_numeric(df['floor_count'], errors='coerce').fillna(0).astype(int)
df['rooms_count'] = pd.to_numeric(df['rooms_count'], errors='coerce').fillna(0).astype(int)

# Преобразование остальных столбцов в float, если это возможно
for column in df.columns:
    if column not in ['floor', 'floor_count', 'rooms_count', 'location']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

# удаляем квартиры с 0 комнат
df = df[df['rooms_count'] != 0]

# Удаление строк, где столбец floor_count равен 1 или 2
df = df[~df['floor_count'].isin([1, 2])]

# вычисляем среднее значение
mean_distance = df['distance'].mean()

# Заполняем NaN значения в столбце 'distance' средним значением
df['distance'] = df['distance'].fillna(mean_distance)

# Заполнение пропусков наиболее частым значением
df['monthly_payment'] = df['monthly_payment'].fillna(df['monthly_payment'].mode()[0])

# удаляем дубликаты
df.drop_duplicates(inplace=True)

# Сохраняем изменения в CSV файл
df.to_csv('cleaned_file.csv', index=False)
