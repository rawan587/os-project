import tkinter as tk
from copy import deepcopy
from rr import round_robin
from srtf import srtf


def build_processes():
    processes = []
    try:
        n = int(num_entry.get())
        for i in range(n):
            arrival = int(arrival_entries[i].get())
            burst = int(burst_entries[i].get())

            processes.append({
                "id": f"P{i+1}",
                "arrival": arrival,
                "burst": burst,
                "remaining": burst,
                "start": -1,
                "completion": 0
            })
        return processes
    except ValueError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please enter valid integer values.\n")
        return None


def draw_gantt(gantt):
    canvas.delete("all")

    if not gantt:
        canvas.create_text(100, 50, text="No Gantt chart to display")
        return

    x = 10
    scale = 30

    for p, start, end in gantt:
        width = (end - start) * scale

        canvas.create_rectangle(x, 30, x + width, 80)
        canvas.create_text(x + width / 2, 55, text=p)

        canvas.create_text(x, 90, text=start)
        x += width

    canvas.create_text(x, 90, text=gantt[-1][2])


def show_comparison(rr_metrics, srtf_metrics):
    for widget in table_frame.winfo_children():
        widget.destroy()

    headers = ["Metric", "RR", "SRTF"]
    for col, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=10, pady=5)

    data = [
        ("Avg WT", rr_metrics["AVERAGE"]["WT"], srtf_metrics["AVERAGE"]["WT"]),
        ("Avg TAT", rr_metrics["AVERAGE"]["TAT"], srtf_metrics["AVERAGE"]["TAT"]),
        ("Avg RT", rr_metrics["AVERAGE"]["RT"], srtf_metrics["AVERAGE"]["RT"]),
    ]

    for i, row in enumerate(data, start=1):
        for j, val in enumerate(row):
            tk.Label(table_frame, text=val).grid(row=i, column=j, padx=10, pady=5)


def run():
    processes = build_processes()
    if processes is None:
        return

    try:
        quantum = int(quantum_entry.get())
    except ValueError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please enter a valid quantum.\n")
        return

    rr_processes = deepcopy(processes)
    srtf_processes = deepcopy(processes)

    rr_gantt, _, rr_metrics = round_robin(rr_processes, quantum)
    srtf_gantt, _, srtf_metrics = srtf(srtf_processes)

    draw_gantt(rr_gantt)
    show_comparison(rr_metrics, srtf_metrics)

    output.delete("1.0", tk.END)
    output.insert(tk.END, "RR GANTT\n")
    output.insert(tk.END, str(rr_gantt) + "\n")
    output.insert(tk.END, str(rr_metrics) + "\n\n")
    output.insert(tk.END, "SRTF GANTT\n")
    output.insert(tk.END, str(srtf_gantt) + "\n")
    output.insert(tk.END, str(srtf_metrics) + "\n")


def create_inputs():
    global arrival_entries, burst_entries

    for widget in inputs_frame.winfo_children():
        widget.destroy()

    arrival_entries = []
    burst_entries = []

    try:
        n = int(num_entry.get())
    except ValueError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please enter a valid number of processes.\n")
        return

    for i in range(n):
        tk.Label(inputs_frame, text=f"P{i+1} Arrival").grid(row=i, column=0, padx=5, pady=5)
        a = tk.Entry(inputs_frame)
        a.grid(row=i, column=1, padx=5, pady=5)

        tk.Label(inputs_frame, text=f"P{i+1} Burst").grid(row=i, column=2, padx=5, pady=5)
        b = tk.Entry(inputs_frame)
        b.grid(row=i, column=3, padx=5, pady=5)

        arrival_entries.append(a)
        burst_entries.append(b)


root = tk.Tk()
root.title("Scheduling Comparison")
root.geometry("900x700")

tk.Label(root, text="Number of Processes").pack()
num_entry = tk.Entry(root)
num_entry.pack()

tk.Label(root, text="Time Quantum").pack()
quantum_entry = tk.Entry(root)
quantum_entry.pack()

inputs_frame = tk.Frame(root)
inputs_frame.pack(pady=10)

canvas = tk.Canvas(root, width=800, height=120, bg="white")
canvas.pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

tk.Button(root, text="Create Inputs", command=create_inputs).pack(pady=5)
tk.Button(root, text="Run Algorithms", command=run).pack(pady=5)

output = tk.Text(root, height=20, width=110)
output.pack(pady=10)

root.mainloop()