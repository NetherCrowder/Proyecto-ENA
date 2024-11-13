import pandas as pd
import numpy as np
from scipy.spatial.distance import mahalanobis

from ..primitives.result import Result
from ..primitives.error import Error
from ..primitives.units import Success

class DiagnosticDataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def calculate_mahalanobis(self, df: pd.DataFrame) -> np.ndarray:
        numeric_cols = df.select_dtypes(include=['float64', 'int64'])
        
        # Verificar si hay NaNs después de la limpieza
        if numeric_cols.isnull().values.any():
            raise ValueError("Existen valores NaN en las columnas numéricas después de la limpieza.")

        # Estandarizar los datos
        standardized_data = (numeric_cols - numeric_cols.mean()) / numeric_cols.std(ddof=0)
        
        # Calcular la matriz de covarianza
        cov_matrix = np.cov(standardized_data.values, rowvar=False)
        
        # Verificar el determinante de la matriz de covarianza
        det = np.linalg.det(cov_matrix)
        if det == 0:
            raise ValueError("La matriz de covarianza es singular y no es invertible.")
        
        # Calcular la inversa de la matriz de covarianza
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        
        mean_vals = np.mean(standardized_data, axis=0)
        mahalanobis_distances = np.apply_along_axis(
            lambda x: mahalanobis(x, mean_vals, inv_cov_matrix), axis=1, arr=standardized_data
        )
        return mahalanobis_distances


    def clean_data(self) -> pd.DataFrame:
        df_cleaned = self.df.copy()
        
        # Mostrar columnas de tipo objeto antes de la conversión
        object_cols = df_cleaned.select_dtypes(include=['object']).columns
        print("Columnas de tipo objeto antes de la conversión:", object_cols)
        
        # Convertir columnas de tipo objeto a numérico si es posible
        df_cleaned[object_cols] = df_cleaned[object_cols].apply(
            lambda col: pd.to_numeric(col, errors='coerce')
        )
        
        # Mostrar columnas con valores NaN después de la conversión
        cols_with_nan = df_cleaned.columns[df_cleaned.isnull().any()].tolist()
        print("Columnas con valores NaN después de la conversión:", cols_with_nan)
        
        # Calcular el porcentaje de valores NaN en cada columna
        nan_percent = df_cleaned.isnull().mean()
        
        # Establecer un umbral para eliminar columnas (por ejemplo, 50%)
        threshold = 0.5
        cols_to_drop = nan_percent[nan_percent > threshold].index
        print("Columnas a eliminar por alto porcentaje de NaN:", cols_to_drop)
        
        # Eliminar las columnas identificadas
        df_cleaned = df_cleaned.drop(columns=cols_to_drop)
        
        # Llenar valores NaN en columnas numéricas con la media
        numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64'])
        df_cleaned[numeric_cols.columns] = numeric_cols.apply(
            lambda x: x.fillna(x.mean()), axis=0
        )
        
        # Eliminar filas con valores NaN restantes en columnas numéricas
        df_cleaned = df_cleaned.dropna(subset=numeric_cols.columns)
        
        # Recalcular las columnas numéricas después de llenar NaNs
        numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64'])
        
        # Recalcular variaciones después de llenar NaNs
        variances = df_cleaned[numeric_cols.columns].var()
        low_variance_cols = variances[variances < 1e-5].index
        print("Columnas con baja varianza a eliminar:", low_variance_cols)
        df_cleaned = df_cleaned.drop(columns=low_variance_cols)
        
        # Actualizar las columnas numéricas después de eliminar las de baja varianza
        numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64'])
        if numeric_cols.empty:
            raise ValueError("No hay columnas numéricas después de eliminar las de baja varianza.")
        
        # Verificar si hay al menos dos filas
        if df_cleaned.shape[0] < 2:
            raise ValueError("Se requieren al menos dos filas en el DataFrame para calcular la distancia de Mahalanobis.")
        
        # Estandarizar los datos
        standardized_data = (df_cleaned[numeric_cols.columns] - df_cleaned[numeric_cols.columns].mean()) / df_cleaned[numeric_cols.columns].std(ddof=0)
        
        # Verificar si aún existen valores NaN después de la estandarización
        if standardized_data.isnull().values.any():
            print("Valores NaN encontrados después de la estandarización.")
            raise ValueError("Existen valores NaN en las columnas numéricas después de la limpieza.")
        
        # Calcular las distancias de Mahalanobis
        mahalanobis_distances = self.calculate_mahalanobis(standardized_data)
        threshold = np.percentile(mahalanobis_distances, 95)
        
        print('MAHALANOBIS=', mahalanobis_distances, '-', threshold)
        
        df_cleaned = df_cleaned[mahalanobis_distances <= threshold]
        
        return df_cleaned

    
    def clean_and_validate_data(self):
        df_cleaned = self.clean_data()

        cleaned_data = df_cleaned.to_dict(orient='records')

        return Result.success(cleaned_data)
