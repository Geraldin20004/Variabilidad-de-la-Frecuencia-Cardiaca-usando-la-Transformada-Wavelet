# Variabilidad-de-la-Frecuencia-Cardiaca-usando-la-Transformada-Wavelet
En nuestro practica de laboratorio como primer paso debiamos realizar una investigacion de los siguientes temas: SNA, la HRV y la transformada wavelet.

 El SNA es responsable de regular funciones fisiológicas involuntarias, como la frecuencia cardíaca, la presión arterial, la digestión y la temperatura corporal. Está compuesto por dos ramas:

-Simpática:  activa el cuerpo en situaciones de alerta o estrés. Aumenta la frecuencia cardíaca, dilata las pupilas y moviliza energía. Se le asocia con la respuesta de “lucha o huida”.

-Parasimpática: favorece el descanso y la recuperación. Disminuye la frecuencia cardíaca y promueve funciones como la digestión y el sueño. Se le conoce como el sistema de “reposo y digestión”.

Estas dos ramas trabajan en conjunto para mantener la homeostasis mediante un equilibrio dinámico.

# Variabilidad de la Frecuencia Cardíaca (HRV)
La HRV (Heart Rate Variability) se refiere a la variación en los intervalos de tiempo entre latidos cardíacos consecutivos, medidos a partir de los intervalos R-R en un ECG,es un indicador sensible de la actividad del sistema nervioso autónomo.

- Una alta (HRV) sugiere una buena capacidad del sistema autónomo para adaptarse a cambios internos o externos, reflejando un predominio parasimpático saludable.
- Una baja (HRV) se ha asociado con estrés, fatiga, enfermedades cardiovasculares y mal pronóstico clínico.

# Análisis espectral de HRV:
Permite dividir la señal en bandas de frecuencia para estimar el predominio simpático o parasimpático:
- Banda de baja frecuencia (LF, 0.04–0.15 Hz): refleja la influencia de ambas ramas, pero con mayor peso simpático.
- Banda de alta frecuencia (HF, 0.15–0.4 Hz): relacionada con la modulación vagal (parasimpática), especialmente influenciada por la respiración.

# Transformada Wavelet
La Transformada Wavelet es una herramienta matemática que permite descomponer una señal en componentes de frecuencia localizados en el tiempo. Es especialmente útil en señales no estacionarias como las biológicas, donde los eventos ocurren de manera transitoria o con patrones que cambian en el tiempo a diferencia de la transformada de Fourier (que analiza todas las frecuencias en conjunto), las wavelets permiten examinar cómo varían las frecuencias a lo largo del tiempo, brindando una visión detallada tiempo-frecuencia.
- Aplicaciones en biomedicina:
Análisis de la HRV, EEG, EMG, y ECG.
Detección de eventos transitorios, patrones anormales y control de calidad de señales.
# Tipos comunes de wavelet:
- Daubechies: ampliamente usadas en señales fisiológicas por su buena resolución y propiedades matemáticas robustas.
- Symlet y Coiflet: versiones modificadas para mayor simetría.
- Morlet: recomendada cuando se requiere alta resolución temporal y frecuencial simultánea.
## CÓDIGO IMPLEMENTADO 

El primer paso fue cargar los datos utilizando tkinter para abrir un cuadro de diálogo y seleccionar un archivo .csv que contenga una señal ECG.

```python
file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
df = pd.read_csv(file_path)
t = df['Tiempo (s)'].to_numpy()
x = df['Voltaje (V)'].to_numpy()
```
Se extraen las columnas de tiempo y voltaje en arreglos de NumPy para su manipulación.

Luego, se procede al diseño del filtro Butterworth pasa banda con frecuencias de corte entre 0.5 Hz y 40 Hz.

```python
b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')
```
- Se muestra la respuesta en frecuencia del filtro.

```python
w, h = freqz(b, a, worN=8000)
plt.plot(...)
```
- Se aplica el filtro manualmente usando la ecuación, permitiendo  implementar el filtrado de la señal ECG con condiciones iniciales en cero.

```python
for n in range(len(x)):
    ...
```
- Para la detección de Picos R: Se detectan los picos R (latidos) con base en su amplitud y separación temporal mínima. Se almacenan los tiempos de ocurrencia.

 ```python
  picos, _ = find_peaks(y, height=0.5, distance=int(0.6 * fs))
```

- Cálculo de intervalos R-R: Se calculan los tiempos entre latidos consecutivos. Son la base para el análisis de HRV.
  
```python
intervalos_rr = np.diff(tiempos_picos)
```

- Para el análisis de HRV en el dominio del tiempo Se calcula:

Media RR: promedio de los intervalos R-R
SDNN: desviación estándar de los intervalos R-R

-Interpolación de R-R: Se interpola la señal RR para obtener un muestreo  necesario para aplicar la transformada wavelet.

```python
fs_interp = 4
tiempo_interp = np.arange(...)
rr_interpolados = interp1d(...)(tiempo_interp)
```
- Padding para Transformada Wavelet Estacionaria (SWT): Se ajusta la longitud de la señal interpolada al múltiplo más cercano de  (nivel deseado = 4), asegurando la compatibilidad con la SWT.

```python
rr_pad = np.pad(...)
t_pad = np.pad(...)
```
- Transformada Wavelet y Análisis LF/HF: Se aplica la SWT con la wavelet Daubechies 4 (db4).

```python  
swt_coeffs = pywt.swt(...)
detail_swt = np.vstack(...)
```
Se calcula la energía de los coeficientes de detalle por nivel:

```python  
energia_por_nivel = [np.sum(cD**2) for (_, cD) in swt_coeffs]
```

##  Resultados
La visualización es una parte esencial del análisis de la variabilidad de la frecuencia cardíaca (HRV), ya que permite interpretar de forma intuitiva los resultados obtenidos en las etapas previas del procesamiento de la señal electrocardiográfica (ECG). En este bloque final del código se generan seis subgráficas agrupadas en una sola figura para observar y comparar fácilmente los distintos aspectos del análisis.

Las gráficas están organizadas en una figura de 3 filas por 2 columnas, abarcando los siguientes aspectos:

### Señal Original vs Señal Filtrada

![image](https://github.com/user-attachments/assets/f61544fa-a85e-45e1-b56c-7c44e3e407d9)
![image](https://github.com/user-attachments/assets/44b63916-6d62-4974-912a-2ab747c2739f)

Esta gráfica compara la señal ECG original (en gris) con la señal filtrada (en azul), la cual ha sido procesada mediante un filtro digital Butterworth pasa banda de 0.5 Hz a 40 Hz. Puesto que se busca eliminar componentes de ruido de baja y alta frecuencia sin alterar la información clínica relevante de la señal. 
Lo cual muestra una señal azul más suave y clara, que conserva los picos R necesarios para el análisis de HRV.

### Detección de Picos R

![image](https://github.com/user-attachments/assets/e22b7860-e743-4252-b869-36a4c3c1ea69)


Esta gráfica muestra los picos R detectados (en rojo) superpuestos sobre la señal ECG filtrada.

-  Se usó la función `find_peaks` de `scipy.signal` para localizar los máximos locales.
- Cabe resaltar que los picos R corresponden a los latidos del corazón. La distancia entre ellos es la base para calcular los intervalos R-R.

### Intervalos R-R

![image](https://github.com/user-attachments/assets/ed25b573-e377-4f70-b9e9-a7925125ffed)


Se grafican los intervalos R-R (en segundos) contra el tiempo promedio entre cada par de picos R consecutivos con el fin de observar la variabilidad temporal de los latidos del corazón ya que una mayor variabilidad suele estar asociada a un buen estado de salud y capacidad de adaptación autonómica.

### Frecuencia Cardíaca Estimada

![image](https://github.com/user-attachments/assets/b88dc201-d8ca-4a86-a482-205fdf7fdd1b)


Aquí se calcula la frecuencia cardíaca instantánea (en bpm) como el inverso de los intervalos R-R:     bpm= 60/ RR(s)
Necesario para evaluar cómo cambia el ritmo cardíaco en el tiempo, además, esta gráfica puede indicar estados de reposo, esfuerzo o alteraciones del ritmo.



### Escalograma SWT (Transformada Wavelet Estacionaria)

![image](https://github.com/user-attachments/assets/3be6bff0-8618-43e7-98dd-8ec8a4c1e479)


-Esta gráfica muestra un mapa de calor (escalograma) generado mediante la **Transformada Wavelet Estacionaria (SWT)** de la señal de intervalos R-R interpolada.
-Se utiliza la wavelet **Daubechies 4 (db4)** para la descomposición.
  * Eje x: Tiempo interpolado.
  * Eje y: Niveles de descomposición (frecuencias), siendo los niveles más altos correspondientes a las frecuencias más bajas (LF).
  * Colores: Magnitud de los coeficientes de detalle (energía en cada frecuencia y momento).
- Permite visualizar cómo varía la actividad cardíaca en distintas bandas de frecuencia a lo largo del tiempo, ofreciendo un análisis tiempo-frecuencia.

### Análisis Adicional del Espectro SWT

Previamente en el código, se calcula la **energía por nivel wavelet**, y se asocian niveles específicos con bandas fisiológicas:

-Nivel 4 (LF):** Banda de baja frecuencia (0.04 - 0.15 Hz), asociada a la actividad simpática.

-Nivel 3 (HF):** Banda de alta frecuencia (0.15 - 0.4 Hz), asociada a la actividad parasimpática.

-La comparación de la energía en ambas bandas permite hacer inferencias sobre el equilibrio autonómico:

 *HF > LF:** Dominio parasimpático (reposo, relajación).
 *LF ≥ HF:** Dominio simpático (estrés, esfuerzo, actividad).




