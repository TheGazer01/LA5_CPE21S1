import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def to_dataframe(history):
    return pd.DataFrame(history, columns=["Method", "Amount (PHP)", "Result"])


def export_csv(history, path):
    to_dataframe(history).to_csv(path, index=False)


def show_chart(parent, history):
    window = tk.Toplevel(parent)
    window.title("Payments per Method")

    figure = Figure(figsize=(5.5, 3.5), dpi=100)
    axes = figure.add_subplot(111)

    if history:
        counts = to_dataframe(history).groupby("Method").size()
        bars = axes.bar(counts.index, counts.values, color="#18bc9c")
        axes.bar_label(bars)
        axes.set_title("Payments per Method")
        axes.set_yticks(range(0, int(counts.max()) + 2))
        axes.tick_params(axis="x", labelrotation=15)
    else:
        axes.text(0.5, 0.5, "No payments yet", ha="center", va="center")
        axes.set_axis_off()

    figure.tight_layout()
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)