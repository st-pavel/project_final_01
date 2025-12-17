import cudf
from cuml.cluster import KMeans
import numpy as np

print("Создаем данные на GPU...")
# Создаем случайные данные сразу в памяти видеокарты
df_gpu = cudf.DataFrame({
    'x': np.random.rand(1000),
    'y': np.random.rand(1000)
})

print("Обучаем KMeans на GPU...")
# Запускаем алгоритм кластеризации (использует CUDA)
kmeans = KMeans(n_clusters=3)
kmeans.fit(df_gpu)

print("Успех! Центроиды кластеров:")
print(kmeans.cluster_centers_)
