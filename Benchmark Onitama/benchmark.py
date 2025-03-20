import time
import gc
import sys

# Importa el código original y optimizado manualmente
# Asegúrate de tener estos dos archivos en el mismo directorio
# original.py - Contiene el código original 
# optimizado.py - Contiene el código optimizado

try:
    # Importar código original
    sys.path.append('.')
    import original
    from original import Nodo, Tarjeta, alpha_beta as alpha_beta_original
    
    # Importar código optimizado
    import optimizado
    from optimizado import Nodo, Tarjeta, alpha_beta as alpha_beta_optimizado
    
    # Función para crear un entorno de prueba
    def crear_entorno_prueba():
        # Tablero inicial de Onitama (5x5)
        tablero = [
            ['-', '-', 'B', '-', '-'],
            ['-', '-', 'b', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', '-', 'w', '-', '-'],
            ['-', '-', 'W', '-', '-']
        ]
        
        # Definir algunas tarjetas de ejemplo
        tarjetas = [
            Tarjeta(0, 1, 1, 0, 2, 0, -1, 0, -2, 0),  # Tiger
            Tarjeta(1, 2, 0, 1, 0, -1, 1, 1, 1, -1),  # Crab
            Tarjeta(-1, 3, 1, 1, -1, 1, 1, -1, -1, -1),  # Mantis
            Tarjeta(0, 4, 1, 0, 0, 1, 0, -1, -1, 0),  # Monkey
            Tarjeta(1, 5, 0, 1, 0, 2, 0, -1, 0, -2)   # Elephant
        ]
        
        # Crear un nodo inicial
        return Nodo(tablero, tarjetas, 0, 0)
    
    # Función principal de prueba
    def test_performance():
        # Crear entorno de prueba común
        nodo_inicial = crear_entorno_prueba()
        
        # Profundidades a probar
        profundidades = [1, 2, 3, 4, 5]
        
        print("=== PRUEBA DE RENDIMIENTO ===")
        
        # Mostrar resultados
        print("\n=== RESULTADOS ===")
        print(f"{'Profundidad':<12} {'Original (ms)':<15} {'Optimizado (ms)':<15} {'Mejora (%)':<15}")
        print("-" * 55)
        
        for profundidad in profundidades:
            # Original
            gc.collect()  # Forzar recolección de basura antes de cada prueba
            tiempo_inicio = time.time()
            alpha_beta_original(nodo_inicial, profundidad, -1000000, 1000000, True, tiempo_inicio, 2000)
            tiempo_fin = time.time()
            tiempo_original = (tiempo_fin - tiempo_inicio) * 1000
            
            # Optimizado
            gc.collect()
            tiempo_inicio = time.time()
            alpha_beta_optimizado(nodo_inicial, profundidad, -1000000, 1000000, True, tiempo_inicio, 2000)
            tiempo_fin = time.time()
            tiempo_optimizado = (tiempo_fin - tiempo_inicio) * 1000
            
            if tiempo_original > 0:
                mejora_porcentaje = ((tiempo_original - tiempo_optimizado) / tiempo_original) * 100
            else:
                mejora_porcentaje = 0
                
            print(f"{profundidad:<12} {tiempo_original:<15.2f} {tiempo_optimizado:<15.2f} {mejora_porcentaje:<15.2f}")
        
        # Ejecutar una prueba específica para profundidad 3 con más repeticiones
        print("\n=== PRUEBA EXTENDIDA (Profundidad 3) ===")
        repeticiones = 10
        
        tiempos_original = []
        tiempos_optimizado = []
        
        for i in range(repeticiones):
            print(f"Repetición {i+1}/{repeticiones}...")
            
            # Original
            gc.collect()
            tiempo_inicio = time.time()
            alpha_beta_original(nodo_inicial, 3, -1000000, 1000000, True, tiempo_inicio, 2000)
            tiempo_fin = time.time()
            tiempos_original.append((tiempo_fin - tiempo_inicio) * 1000)
            
            # Optimizado
            gc.collect()
            tiempo_inicio = time.time()
            alpha_beta_optimizado(nodo_inicial, 3, -1000000, 1000000, True, tiempo_inicio, 2000)
            tiempo_fin = time.time()
            tiempos_optimizado.append((tiempo_fin - tiempo_inicio) * 1000)
        
        # Calcular promedios
        promedio_original = sum(tiempos_original) / len(tiempos_original)
        promedio_optimizado = sum(tiempos_optimizado) / len(tiempos_optimizado)
        mejora_porcentaje = ((promedio_original - promedio_optimizado) / promedio_original) * 100
        
        print("\nResultados finales (promedio de 10 repeticiones):")
        print(f"Código original: {promedio_original:.2f} ms")
        print(f"Código optimizado: {promedio_optimizado:.2f} ms")
        print(f"Mejora: {mejora_porcentaje:.2f}%")
        
except Exception as e:
    print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_performance()