
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from rr2 import round_robin
from srtf import srtf


def build_processes():
    processes = []
    ids = set()

    try:
        n = int(num_entry.get())

        for i in range(n):
            pid = id_entries[i].get().strip()
            arrival = int(arrival_entries[i].get())
            burst = int(burst_entries[i].get())

           
            if pid == "":
                messagebox.showerror("Error", "Process ID cannot be empty")
                return None

            if pid in ids:
                messagebox.showerror("Error", f"Duplicate ID: {pid}")
                return None
            ids.add(pid)

          
            if arrival < 0:
                messagebox.showerror("Error", f"Arrival time of {pid} cannot be negative")
                return None

            
            if burst <= 0:
                messagebox.showerror("Error", f"Burst time of {pid} must be positive")
                return None

            processes.append({
                "id": pid,
                "arrival": arrival,
                "burst": burst,
                "remaining": burst,
                "start": -1,
                "completion": 0
            })

        return processes

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")
        return None


def draw_gantt(gantt):
    canvas.delete("all")

    if not gantt:
        canvas.create_text(200, 50, text="No Gantt chart")
        return

    x = 10
    scale = 30

    for p, start, end in gantt:
        width = (end - start) * scale

        canvas.create_rectangle(x, 30, x + width, 80, fill="lightblue")
        canvas.create_text(x + width / 2, 55, text=p)

        canvas.create_text(x, 90, text=start)

        x += width + 10 
    canvas.create_text(x, 90, text=gantt[-1][2])


def show_table(frame, title, metrics):
    tk.Label(frame, text=title, font=("Arial", 12, "bold")).pack()

    headers = ["Process", "WT", "TAT", "RT"]
    row_frame = tk.Frame(frame)
    row_frame.pack()

    for h in headers:
        tk.Label(row_frame, text=h, width=10, font=("Arial", 10, "bold")).pack(side="left")

    for pid, data in metrics.items():
        if pid == "AVERAGE":
            continue

        row = tk.Frame(frame)
        row.pack()

        tk.Label(row, text=pid, width=10).pack(side="left")
        tk.Label(row, text=data["WT"], width=10).pack(side="left")
        tk.Label(row, text=data["TAT"], width=10).pack(side="left")
        tk.Label(row, text=data["RT"], width=10).pack(side="left")


def show_comparison(rr_metrics, srtf_metrics):
    for widget in table_frame.winfo_children():
        widget.destroy()

    show_table(table_frame, "Round Robin Results", rr_metrics)
    show_table(table_frame, "SRTF Results", srtf_metrics)

    rr_wt = rr_metrics["AVERAGE"]["WT"]
    srtf_wt = srtf_metrics["AVERAGE"]["WT"]

    better = "RR" if rr_wt < srtf_wt else "SRTF"

    tk.Label(table_frame,
             text=f"\nBetter Algorithm: {better}",
             font=("Arial", 12, "bold"),
             fg="green").pack()


def run():
    processes = build_processes()
    if processes is None:
        return

    try:
        quantum = int(quantum_entry.get())
        if quantum < 1 or quantum > 100:
            messagebox.showerror("Error", "Quantum must be between 1 and 100")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid Quantum")
        return

    rr_processes = deepcopy(processes)
    srtf_processes = deepcopy(processes)

    rr_gantt, rr_queue, rr_metrics = round_robin(rr_processes, quantum)
    srtf_gantt, _, srtf_metrics = srtf(srtf_processes)

    draw_gantt(rr_gantt)
    show_comparison(rr_metrics, srtf_metrics)

   
    queue_text.delete("1.0", tk.END)
    queue_text.insert(tk.END, "Ready Queue (RR):\n")
    for q in rr_queue:
        queue_text.insert(tk.END, str(q) + "\n")

    output.delete("1.0", tk.END)
    output.insert(tk.END, "RR Gantt:\n" + str(rr_gantt) + "\n\n")
    output.insert(tk.END, "SRTF Gantt:\n" + str(srtf_gantt) + "\n")


def create_inputs():
    global arrival_entries, burst_entries, id_entries

    for widget in inputs_frame.winfo_children():
        widget.destroy()

    arrival_entries = []
    burst_entries = []
    id_entries = []

    try:
        n = int(num_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid number of processes")
        return

    for i in range(n):
        tk.Label(inputs_frame, text=f"ID").grid(row=i, column=0)
        pid = tk.Entry(inputs_frame)
        pid.grid(row=i, column=1)

        tk.Label(inputs_frame, text="Arrival").grid(row=i, column=2)
        a = tk.Entry(inputs_frame)
        a.grid(row=i, column=3)

        tk.Label(inputs_frame, text="Burst").grid(row=i, column=4)
        b = tk.Entry(inputs_frame)
        b.grid(row=i, column=5)

        id_entries.append(pid)
        arrival_entries.append(a)
        burst_entries.append(b)



root = tk.Tk()
root.title("CPU Scheduling")
root.geometry("1000x750")

tk.Label(root, text="Number of Processes").pack()
num_entry = tk.Entry(root)
num_entry.pack()

tk.Label(root, text="Time Quantum").pack()
quantum_entry = tk.Entry(root)
quantum_entry.pack()

inputs_frame = tk.Frame(root)
inputs_frame.pack(pady=10)


canvas_frame = tk.Frame(root)
canvas_frame.pack()

canvas = tk.Canvas(canvas_frame, width=900, height=120, bg="white")
scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)

canvas.configure(xscrollcommand=scroll_x.set)

canvas.pack()
scroll_x.pack(fill="x")

table_frame = tk.Frame(root)
table_frame.pack(pady=10)


queue_text = tk.Text(root, height=6, width=50)
queue_text.pack()

tk.Button(root, text="Create Inputs", command=create_inputs).pack(pady=5)
tk.Button(root, text="Run", command=run).pack(pady=5)

output_frame = tk.Frame(root)
output_frame.pack()

output = tk.Text(output_frame, height=10, width=110)
scroll_y = tk.Scrollbar(output_frame, command=output.yview)

output.configure(yscrollcommand=scroll_y.set)

output.pack(side="left")
scroll_y.pack(side="right", fill="y")

root.mainloop()