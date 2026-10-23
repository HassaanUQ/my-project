import serial
import matplotlib.pyplot as plt
from drawnow import *

# === Setup Serial ===
# Note: If running on Windows, change '/dev/ttyACM0' to your COM port (e.g., 'COM3')
sinWaveData = serial.Serial('/dev/ttyACM0', 115200)
plt.ion()

# === Plot Styles to Rotate Through ===
plot_styles = ['r.-', 'b.-', 'g.-', 'm.-', 'c.-', 'y.-', 'k.-']

# === Data Storage ===
NUM_SAMPLES = 100
time_ms = []
cnt = 0
all_signals = []  # List of lists for X, Y, Z values
signals = ["X", "Y", "Z"]  # Updated to match X, Y, Z output

# === Plotting Function ===
def makeFig(title, xLabel, yLabel, yLimit, *args):
    plt.clf()
    plt.title(title)
    plt.grid(True)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.ylim(yLimit[0], yLimit[1])  

    for arg in args:
        plt.plot(time_ms, arg[0], arg[1], label=arg[2])

    plt.legend(loc='upper left')

# === Main Loop ===
while True:
    while sinWaveData.inWaiting() == 0:
        pass  # Wait for data

    try:
        line = sinWaveData.readline().decode().strip()
        values = line.split(',')

        # First time: initialize sublists based on number of incoming values
        if len(all_signals) != len(values):
            all_signals = [[] for _ in range(len(values))]

        # Append each value to its corresponding signal list
        for i, val in enumerate(values):
            all_signals[i].append(float(val))

        time_ms.append(cnt)
        cnt += 1

        # Build args for plotting
        args = []
        for i, signal in enumerate(all_signals):
            style = plot_styles[i % len(plot_styles)]
            # Safeguard if more/less values arrive than expected
            label = signals[i] if i < len(signals) else f"Signal {i}"
            args.append((signal, style, label))

        title = "Accelerometer X, Y, Z Plot"
        drawnow(lambda: makeFig(title, "Time (ms)", "Value / g", [-2, 2], *args))
        plt.pause(0.001)

        # Keep only last NUM_SAMPLES samples
        if len(time_ms) > NUM_SAMPLES:
            time_ms.pop(0)
            for signal in all_signals:
                signal.pop(0)

    except Exception as e:
        print("Error:", e)