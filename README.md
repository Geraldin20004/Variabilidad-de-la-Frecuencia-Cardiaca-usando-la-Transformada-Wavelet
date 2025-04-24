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
