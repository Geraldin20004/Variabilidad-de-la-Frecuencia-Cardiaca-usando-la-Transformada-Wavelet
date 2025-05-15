import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz, find_peaks
from scipy.interpolate import interp1d
import pywt
from tkinter.filedialog import askopenfilename

# ----------------------------
# 1) Cargar datos
# ----------------------------
file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
df = pd.read_csv(file_path)

print("Columnas encontradas en el archivo:")
print(df.columns)

# Ajustar según las columnas reales
t = df['Tiempo (s)'].to_numpy()
x = df['Voltaje (V)'].to_numpy()

# ----------------------------
# 2) Filtro Butterworth pasa banda
# ----------------------------
fs = 1000  # Hz
lowcut, highcut, order = 0.5, 40, 4
nyq = 0.5 * fs
b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')

# Mostrar respuesta en frecuencia del filtro
w, h = freqz(b, a, worN=8000)
plt.figure()
plt.plot(0.5 * fs * w / np.pi, abs(h), 'b')
plt.title('Respuesta en Frecuencia del Filtro Butterworth')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Ganancia')
plt.grid()
plt.tight_layout()
plt.show()

# Implementación manual de la ecuación en diferencias (condiciones iniciales 0)
y = np.zeros_like(x)
for n in range(len(x)):
    for i in range(len(b)):
        if n - i >= 0:
            y[n] += b[i] * x[n - i]
    for j in range(1, len(a)):
        if n - j >= 0:
            y[n] -= a[j] * y[n - j]

# ----------------------------
# 3) Detección de Picos R
# ----------------------------
picos, _ = find_peaks(y, height=0.5, distance=int(0.6 * fs))
tiempos_picos = t[picos]

# ----------------------------
# 4) Intervalos R-R
# ----------------------------
intervalos_rr = np.diff(tiempos_picos)
tiempos_rr = (tiempos_picos[:-1] + tiempos_picos[1:]) / 2

# ----------------------------
# 5) HRV en dominio del tiempo
# ----------------------------
print("\n--- HRV Dominio del tiempo ---")
print(f"Media RR: {intervalos_rr.mean():.4f} s   SDNN: {intervalos_rr.std():.4f} s")

plt.figure()
plt.hist(intervalos_rr, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de Intervalos R-R')
plt.xlabel('RR (s)')
plt.ylabel('Frecuencia')
plt.grid()
plt.tight_layout()
plt.show()

# ----------------------------
# 6) Interpolación de R-R
# ----------------------------
fs_interp = 4  # Hz para HRV
tiempo_interp = np.arange(tiempos_rr[0], tiempos_rr[-1], 1/fs_interp)
rr_interpolados = interp1d(tiempos_rr, intervalos_rr, kind='cubic')(tiempo_interp)

# ----------------------------
# 7) Padding para SWT
# ----------------------------
desired_levels = 4
base = 2**desired_levels
L0 = len(rr_interpolados)
Lpad = ((L0 - 1)//base + 1)*base

pad_width = Lpad - L0
rr_pad = np.pad(rr_interpolados, (0, pad_width), 'edge')
t_pad  = np.pad(
    tiempo_interp,
    (0, pad_width),
    mode='linear_ramp',
    end_values=(tiempo_interp[-1],
                tiempo_interp[-1] + pad_width*(1/fs_interp))
)

# ----------------------------
# 8) Transformada Wavelet (SWT) y análisis LF/HF
# ----------------------------
waveletname = 'db4'
swt_coeffs = pywt.swt(rr_pad, waveletname, level=desired_levels)
detail_swt = np.vstack([cD for (_ , cD) in swt_coeffs])  # shape (levels, Lpad)

# Calcular energía por nivel
energia_por_nivel = [np.sum(cD**2) for (_, cD) in swt_coeffs]
niveles = list(range(1, desired_levels+1))

# Graficar energía por nivel
plt.figure()
plt.bar(niveles, energia_por_nivel, color='orchid')
plt.xticks(niveles)
plt.title("Energía por Nivel SWT")
plt.xlabel("Nivel")
plt.ylabel("Energía")
plt.grid(True)
plt.tight_layout()
plt.show()

# Análisis de LF (nivel 4) y HF (nivel 3)
energia_lf = energia_por_nivel[3]  # nivel 4
energia_hf = energia_por_nivel[2]  # nivel 3
print("\n--- Análisis Frecuencias ---")
print(f"Energía banda LF (nivel 4): {energia_lf:.4f}")
print(f"Energía banda HF (nivel 3): {energia_hf:.4f}")
if energia_hf > energia_lf:
    print("Predomina la actividad parasimpática (HF > LF).")
else:
    print("Predomina la actividad simpática o estrés (LF ≥ HF).")

# ----------------------------
# 9) Gráficos completos
# ----------------------------
plt.figure(figsize=(14, 10))

plt.subplot(3, 2, 1)
plt.plot(t, x, label='Original', color='gray')
plt.plot(t, y, label='Filtrada', color='blue')
plt.title('Señal Original vs Filtrada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 2)
plt.plot(t, y, label='Filtrada')
plt.plot(tiempos_picos, y[picos], 'ro', label='Picos R')
plt.title('Detección de Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 3)
plt.plot(tiempos_rr, intervalos_rr, 'o-')
plt.title('Intervalos R-R')
plt.xlabel('Tiempo (s)')
plt.ylabel('RR (s)')
plt.grid(True)

plt.subplot(3, 2, 4)
plt.plot(tiempos_rr, 60/intervalos_rr, 'g.-')
plt.title('Frecuencia Cardíaca Estimada')
plt.xlabel('Tiempo (s)')
plt.ylabel('bpm')
plt.grid(True)

plt.subplot(3, 2, 5)
plt.hist(intervalos_rr, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de Intervalos R-R')
plt.xlabel('RR (s)')
plt.ylabel('Frecuencia')
plt.grid(True)

plt.subplot(3, 2, 6)
extent = [t_pad[0], t_pad[-1], desired_levels, 1]
img = plt.imshow(
    np.abs(detail_swt),
    extent=extent,
    aspect='auto',
    cmap='jet',
    origin='lower',
    vmin=0,
    vmax=np.percentile(np.abs(detail_swt), 99)
)
plt.title(f'Escalograma SWT ({waveletname})')
plt.xlabel('Tiempo (s)')
plt.ylabel('Nivel SWT')
plt.colorbar(img, label='|Coef detalle|')

plt.tight_layout()
plt.show()
