# Импортируем библиотеки
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загружаем CSV файл
df = pd.read_csv('cleaned_file.csv')

# Построение матрицы корреляции
correlation_matrix = df[['square_meter_price', 'area', 'floor', 'floor_count', 'rooms_count', 'distance', 'monthly_payment']].corr()

# Визуализация корреляционной матрицы
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", annot_kws={"size": 10})
plt.xticks(rotation=70, fontsize=10)
plt.title("Корреляция между переменными")

plt.savefig('correlation_matrix.png')

