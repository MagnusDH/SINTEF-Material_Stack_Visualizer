import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph():
    # Data for plotting
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    # Create a new figure
    fig = Figure(figsize=(5, 4), dpi=100)

    # Add a subplot
    plot = fig.add_subplot(1, 1, 1)

    # Plot the data
    plot.plot(x, y)

    # Set labels
    plot.set_xlabel('X Axis')
    plot.set_ylabel('Y Axis')
    plot.set_title('Sample Graph')

    # Create Tkinter canvas widget
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # Display canvas
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a Tkinter window
root = tk.Tk()
root.title("Tkinter Graph Example")

# Button to plot graph
plot_button = tk.Button(root, text="Plot Graph", command=plot_graph)
plot_button.pack(side=tk.BOTTOM)

# Run the Tkinter event loop
root.mainloop()
