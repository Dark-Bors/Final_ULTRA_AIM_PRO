# visualization_panel.py
# This file defines the panel for data visualization.

import tkinter as tk
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Scrollbar, Frame, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app_logging import logger


class VisualizationPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(borderwidth=2, relief='sunken')
        logger.info("ℹ️ Initializing the VisualizationPanel.")
        self.master = master

        # Set grid weight configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a canvas with a scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        # Configure the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind the canvas configuration to an event
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Place the widgets using grid
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Initialize variables to store figures and canvases
        self.figures = []
        self.canvases = []
    

    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Resize the inner frame to match the canvas
        self.canvas.itemconfig("self.scrollable_frame", width=event.width)

        # Update the canvas scrolling region
        self.on_frame_configure()

    def plot_loss(self, history):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.clear()
        ax.plot(history.history['loss'], label='Train Loss')
        ax.plot(history.history['val_loss'], label='Validation Loss')
        ax.set_title('Training & Validation Loss')
        ax.set_ylabel('Loss')
        ax.set_xlabel('Epoch')
        ax.legend(loc='upper right')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)

        # Store the figure and canvas
        self.figures.append(fig)
        self.canvases.append(canvas)

    def plot_predictions(self, y_test, predicted_reliability):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.clear()
        ax.scatter(y_test, predicted_reliability, label='Predicted Reliability')
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4, label='Perfect Prediction')
        ax.set_xlabel('True Values [Reliability]')
        ax.set_ylabel('Predictions [Reliability]')
        ax.set_title('Prediction Accuracy')
        ax.legend(loc='upper left')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)

        # Store the figure and canvas
        self.figures.append(fig)
        self.canvases.append(canvas)

    def plot_parameter_impact(self, X_test, y_test, predicted_reliability, feature_names):
        # Determine the layout of the subplots
        num_features = len(feature_names)
        num_cols = 2
        num_rows = int(np.ceil(num_features / num_cols))
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, num_rows * 4))

        for i, feature_name in enumerate(feature_names):
            ax = axs[i // num_cols, i % num_cols]
            ax.scatter(X_test[:, i], predicted_reliability, label='Predicted Reliability')
            ax.scatter(X_test[:, i], y_test, color='red', label='Actual Reliability', alpha=0.5)
            ax.set_xlabel(feature_name)
            ax.set_ylabel('Reliability')
            ax.set_title(f'Impact of {feature_name}')
            ax.legend()
            ax.grid(True)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)

        # Store the figure and canvas
        self.figures.append(fig)
        self.canvases.append(canvas)

    def clear_plots(self):
        logger.info("ℹ️ Clearing plots.")
        for canvas in self.canvases:
            canvas.get_tk_widget().pack_forget()
            canvas.get_tk_widget().destroy()
        self.figures.clear()
        self.canvases.clear()
        logger.debug("🐛 Plots cleared from the visualization panel.")


    def get_graph_data(self):
        # Extract data from the figures for saving to MATLAB
        data = {}
        for idx, fig in enumerate(self.figures):
            # Assuming your data is plotted as line plots
            ax = fig.axes[0]
            for line in ax.get_lines():
                label = line.get_label()
                if label not in ['_nolegend_']:
                    x_data, y_data = line.get_data()
                    data[f'figure_{idx}_{label}_x'] = x_data
                    data[f'figure_{idx}_{label}_y'] = y_data
        return data

    def save_graphs_for_matlab(self, file_path):
        # Save the graph data to a MATLAB .mat file
        data = self.get_graph_data()
        print("data is:", data)
        scipy.io.savemat(file_path, data)

    def save_graphs_as_image(self, file_path, fig):
        # Save the graph as an image
        fig.savefig(file_path)
    
    
    def save_graphs_interactive(self):
        # Save the current figure for interactive use
        file_path = filedialog.asksaveasfilename(title="Save Interactive Graph", 
                                                filetypes=[("All Files", "*.*")],
                                                defaultextension="")
        if file_path:
            # You can use a different format like .pickle, .mat, etc.
            pass