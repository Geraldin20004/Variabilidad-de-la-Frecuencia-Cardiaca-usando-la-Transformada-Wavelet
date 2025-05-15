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
##  Resultados
La visualización es una parte esencial del análisis de la variabilidad de la frecuencia cardíaca (HRV), ya que permite interpretar de forma intuitiva los resultados obtenidos en las etapas previas del procesamiento de la señal electrocardiográfica (ECG). En este bloque final del código se generan seis subgráficas agrupadas en una sola figura para observar y comparar fácilmente los distintos aspectos del análisis.

Las gráficas están organizadas en una figura de 3 filas por 2 columnas, abarcando los siguientes aspectos:

### Señal Original vs Señal Filtrada

Esta gráfica compara la señal ECG original (en gris) con la señal filtrada (en azul), la cual ha sido procesada mediante un filtro digital Butterworth pasa banda de 0.5 Hz a 40 Hz.

* **Objetivo:** Eliminar componentes de ruido de baja y alta frecuencia sin alterar la información clínica relevante de la señal.
* **Resultado esperado:** Una señal azul más suave y clara, que conserva los picos R necesarios para el análisis de HRV.

### Detección de Picos R

Esta gráfica muestra los picos R detectados (en rojo) superpuestos sobre la señal ECG filtrada.

* **Técnica utilizada:** Se usa la función `find_peaks` de `scipy.signal` para localizar los máximos locales.
* **Importancia:** Los picos R corresponden a los latidos del corazón. La distancia entre ellos es la base para calcular los intervalos R-R.

### Intervalos R-R

Se grafican los intervalos R-R (en segundos) contra el tiempo promedio entre cada par de picos R consecutivos.

* **Objetivo:** Observar la variabilidad temporal de los latidos del corazón.
* **Significado fisiológico:** Una mayor variabilidad suele estar asociada a un buen estado de salud y capacidad de adaptación autonómica.

### Frecuencia Cardíaca Estimada

Aquí se calcula la frecuencia cardíaca instantánea (en bpm) como el inverso de los intervalos R-R:
$\text{bpm} = \frac{60}{\text{RR (s)}}$

* **Objetivo:** Evaluar cómo cambia el ritmo cardíaco en el tiempo.
* **Aplicación clínica:** Esta gráfica puede indicar estados de reposo, esfuerzo o alteraciones del ritmo.

### 📊 9.5 Histograma de Intervalos R-R

Muestra la distribución de los valores de intervalos R-R en forma de histograma.

* **Interpretación:** Una distribución estrecha indica ritmo regular; una distribución amplia refleja mayor variabilidad, característica deseable en condiciones fisiológicas normales.

### Escalograma SWT (Transformada Wavelet Estacionaria)

Esta gráfica muestra un mapa de calor (escalograma) generado mediante la **Transformada Wavelet Estacionaria (SWT)** de la señal de intervalos R-R interpolada.

* **Herramienta:** Se utiliza la wavelet **Daubechies 4 (db4)** para la descomposición.
* **Ejes:**

  * Eje x: Tiempo interpolado.
  * Eje y: Niveles de descomposición (frecuencias), siendo los niveles más altos correspondientes a las frecuencias más bajas (LF).
  * Colores: Magnitud de los coeficientes de detalle (energía en cada frecuencia y momento).
* **Utilidad:** Permite visualizar cómo varía la actividad cardíaca en distintas bandas de frecuencia a lo largo del tiempo, ofreciendo un análisis tiempo-frecuencia.

### Análisis Adicional del Espectro SWT

Previamente en el código, se calcula la **energía por nivel wavelet**, y se asocian niveles específicos con bandas fisiológicas:

* **Nivel 4 (LF):** Banda de baja frecuencia (0.04 - 0.15 Hz), asociada a la actividad simpática.
* **Nivel 3 (HF):** Banda de alta frecuencia (0.15 - 0.4 Hz), asociada a la actividad parasimpática.

La comparación de la energía en ambas bandas permite hacer inferencias sobre el equilibrio autonómico:

* **HF > LF:** Dominio parasimpático (reposo, relajación).
* **LF ≥ HF:** Dominio simpático (estrés, esfuerzo, actividad).

---

En conjunto, estas visualizaciones permiten realizar un análisis integral de la señal ECG y la HRV, facilitando la interpretación fisiológica desde el dominio del tiempo y el dominio tiempo-frecuencia.

