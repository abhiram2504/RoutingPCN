import matplotlib.pyplot as plt
import numpy as np

data = {
    "Plot 1": {
        "LSST_x": [17.99, 39.07, 44.7, 49.8, 62.34, 77.21],
        "LSST_y": [1, 1, 1, 0.89, 0.63, 0.41],
        "Shortest_x": [17.99, 39.07, 44.7, 49.8, 62.34, 77.21],
        "Shortest_y": [0.97, 0.95, 0.94, 0.94, 0.93, 0.89]
    },
    "Plot 2": {
        "LSST_x": [15.27, 26.04, 34.14, 39.17, 42.09, 43.93],
        "LSST_y": [1, 1, 1, 0.84, 0.68, 0.49],
        "Shortest_x": [15.27, 26.04, 34.14, 39.17, 42.09, 43.93],
        "Shortest_y": [0.96, 0.92, 0.88, 0.85, 0.79, 0.77]
    },
    "Plot 3": {
        "LSST_x": [17.99, 39.07, 44.7, 49.8, 62.34, 77.21],
        "LSST_y": [1, 1, 0.99, 0.83, 0.60, 0.35],
        "Shortest_x": [17.99, 39.07, 44.7, 49.8, 62.34, 77.21],
        "Shortest_y": [0.91, 0.90, 0.88, 0.86, 0.70, 0.49]
    },
    "Plot 4": {
        "LSST_x": [15.27, 26.04, 34.14, 39.17, 42.09, 43.93],
        "LSST_y": [1, 1, 1, 0.73, 0.5, 0.38],
        "Shortest_x": [15.27, 26.04, 34.14, 39.17, 42.09, 43.93],
        "Shortest_y": [0.88, 0.88, 0.83, 0.76, 0.60, 0.50]
    }
}

fig, axs = plt.subplots(2, 2, figsize=(12, 12))
axs = axs.flatten()  

for i, (plot_name, plot_data) in enumerate(data.items()):
    bar_width = 0.35
    x = np.array(plot_data['LSST_x'])
    ls_y = plot_data['LSST_y']
    shortest_y = plot_data['Shortest_y']
    
    index = np.arange(len(x))

    axs[i].bar(index - bar_width/2, ls_y, bar_width, label='LSST', color='blue')
    axs[i].bar(index + bar_width/2, shortest_y, bar_width, label='Shortest', color='green')
    
    axs[i].set_xlabel('Demand Density', fontsize=12)
    axs[i].set_ylabel('Throughput', fontsize=12)
    axs[i].set_title(plot_name, fontsize=14)
    axs[i].set_xticks(index)
    axs[i].set_xticklabels(x)
    axs[i].legend()


plt.tight_layout()
plt.show()
