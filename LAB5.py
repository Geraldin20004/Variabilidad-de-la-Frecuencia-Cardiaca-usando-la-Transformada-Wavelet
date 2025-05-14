import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, find_peaks
from scipy.interpolate import interp1d
import pywt
from tkinter.filedialog import askopenfilename

# ----------------------------
# 1) Cargar datos
# ----------------------------
file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
df = pd.read_csv(file_path)

# Mostrar nombres reales de columnas
print("Columnas encontradas en el archivo:")
print(df.columns)

# Ajusta los nombres de columna aquí según lo que imprima arriba
# Por ejemplo, si ves 'Tiempo (s)' y 'Voltaje (V)', usa esos nombres
t = df['Tiempo (s)'].to_numpy()  # Mantén la columna 'Tiempo (s)'
x = df['Voltaje (V)'].to_numpy()  # Cambia 'Señal' por 'Voltaje (V)'

# ----------------------------
# 2) Filtro Butterworth pasa banda
# ----------------------------
fs = 1000  # Hz
lowcut, highcut, order = 0.5, 40, 4
nyq = 0.5 * fs
b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')

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
# 4) Cálculo de Intervalos R-R
# ----------------------------
intervalos_rr = np.diff(tiempos_picos)
tiempos_rr = (tiempos_picos[:-1] + tiempos_picos[1:]) / 2

# ----------------------------
# 5) HRV en dominio del tiempo
# ----------------------------
print("\n--- HRV Dominio del tiempo ---")
print(f"Media RR: {intervalos_rr.mean():.4f} s   SDNN: {intervalos_rr.std():.4f} s")

plt.figure(figsize=(8, 4))
plt.hist(intervalos_rr, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de Intervalos R-R')
plt.xlabel('RR (s)')
plt.ylabel('Frecuencia')
plt.grid(True)
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
# 8) Escalograma SWT (Daubechies 4)
# ----------------------------
waveletname = 'db4'
swt_coeffs = pywt.swt(rr_pad, waveletname, level=desired_levels)
detail_swt = np.vstack([cD for (_ , cD) in swt_coeffs])  # shape (levels, Lpad)

# Preparar extent para imshow evitando ylims idénticos
y0, y1 = (desired_levels, 1) if desired_levels > 1 else (0.5, 1.5)
extent = [t_pad[0], t_pad[-1], y0, y1]

# ----------------------------
# 9) Gráficos de señal, RR y escalograma
# ----------------------------
plt.figure(figsize=(14, 10))

# 9.1 Señal original vs filtrada
plt.subplot(3, 2, 1)
plt.plot(t, x, color='gray', label='Original')
plt.plot(t, y, color='blue', label='Filtrada')
plt.title('Original vs Filtrada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)

# 9.2 Picos R
plt.subplot(3, 2, 2)
plt.plot(t, y, label='Filtrada')
plt.plot(tiempos_picos, y[picos], 'ro', label='Picos R')
plt.title('Detección de Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)

# 9.3 Intervalos R-R en el tiempo
plt.subplot(3, 2, 3)
plt.plot(tiempos_rr, intervalos_rr, 'o-')
plt.title('Intervalos R-R')
plt.xlabel('Tiempo (s)')
plt.ylabel('RR (s)')
plt.grid(True)

# 9.4 Frecuencia cardíaca estimada
plt.subplot(3, 2, 4)
plt.plot(tiempos_rr, 60/intervalos_rr, 'g.-')
plt.title('Frecuencia Cardíaca Estimada')
plt.xlabel('Tiempo (s)')
plt.ylabel('bpm')
plt.grid(True)

# 9.5 Histograma de R-R
plt.subplot(3, 2, 5)
plt.hist(intervalos_rr, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de Intervalos R-R')
plt.xlabel('RR (s)')
plt.ylabel('Frecuencia')
plt.grid(True)

# 9.6 Escalograma SWT
plt.subplot(3, 2, 6)
img = plt.imshow(
    np.abs(detail_swt),
    extent=extent,
    aspect='auto',
    cmap='jet',
    origin='lower',
    vmin=0,
    vmax=np.percentile(np.abs(detail_swt), 99)
)
plt.title(f'Escalograma SWT (db4)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Nivel SWT')
plt.colorbar(img, label='|Coef detalle|')

plt.tight_layout()
plt.show()

