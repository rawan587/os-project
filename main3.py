
# import tkinter as tk
# from tkinter import messagebox
# from copy import deepcopy
# from rr2 import round_robin
# from srtf import srtf
# from utils import calculate_metrics

# def calculate_metrics(processes):
#     metrics = {}
#     total_wt = total_tat = total_rt = 0
#     n = len(processes)

#     for p in processes:
#         tat = p["completion"] - p["arrival"]
#         wt = tat - p["burst"]
#         rt = p["start"] - p["arrival"]

#         metrics[p["id"]] = {
#             "WT": wt,
#             "TAT": tat,
#             "RT": rt
#         }

#         total_wt += wt
#         total_tat += tat
#         total_rt += rt

#     metrics["AVERAGE"] = {
#         "WT": total_wt / n,
#         "TAT": total_tat / n,
#         "RT": total_rt / n
#     }

#     return metrics



# def build_processes():
#     processes = []
#     ids = set()

#     try:
#         n = int(num_entry.get())

#         for i in range(n):
#             pid = id_entries[i].get().strip()
#             arrival = int(arrival_entries[i].get())
#             burst = int(burst_entries[i].get())

#             if pid == "":
#                 messagebox.showerror("Error", "Process ID cannot be empty")
#                 return None

#             if pid in ids:
#                 messagebox.showerror("Error", f"Duplicate ID: {pid}")
#                 return None
#             ids.add(pid)

#             if arrival < 0:
#                 messagebox.showerror("Error", f"Arrival time of {pid} cannot be negative")
#                 return None

#             if burst <= 0:
#                 messagebox.showerror("Error", f"Burst time of {pid} must be positive")
#                 return None

#             processes.append({
#                 "id": pid,
#                 "arrival": arrival,
#                 "burst": burst,
#                 "remaining": burst,
#                 "start": -1,
#                 "completion": 0
#             })

#         return processes

#     except ValueError:
#         messagebox.showerror("Error", "Enter valid numbers")
#         return None



# def draw_gantt(gantt, y_offset=0, title=""):
#     canvas.create_text(50, 10 + y_offset, text=title, anchor="w", font=("Arial", 10, "bold"))

#     if not gantt:
#         return

#     x = 10
#     scale = 30

#     for p, start, end in gantt:
#         width = (end - start) * scale

#         canvas.create_rectangle(x, 30 + y_offset, x + width, 80 + y_offset, fill="lightblue")
#         canvas.create_text(x + width / 2, 55 + y_offset, text=p)

#         canvas.create_text(x, 90 + y_offset, text=start)

#         x += width + 10

#     canvas.create_text(x, 90 + y_offset, text=gantt[-1][2])

#     canvas.configure(scrollregion=canvas.bbox("all"))



# def show_table(frame, title, metrics):
#     tk.Label(frame, text=title, font=("Arial", 12, "bold")).pack()

#     headers = ["Process", "WT", "TAT", "RT"]
#     row_frame = tk.Frame(frame)
#     row_frame.pack()

#     for h in headers:
#         tk.Label(row_frame, text=h, width=10, font=("Arial", 10, "bold")).pack(side="left")

 
#     for pid, data in metrics.items():
#         if pid == "AVERAGE":
#             continue

#         row = tk.Frame(frame)
#         row.pack()

#         tk.Label(row, text=pid, width=10).pack(side="left")
#         tk.Label(row, text=data["WT"], width=10).pack(side="left")
#         tk.Label(row, text=data["TAT"], width=10).pack(side="left")
#         tk.Label(row, text=data["RT"], width=10).pack(side="left")

#     avg = metrics["AVERAGE"]

#     avg_row = tk.Frame(frame)
#     avg_row.pack(pady=5)

#     tk.Label(avg_row, text="AVG", width=10, fg="blue", font=("Arial", 10, "bold")).pack(side="left")
#     tk.Label(avg_row, text=avg["WT"], width=10, fg="blue").pack(side="left")
#     tk.Label(avg_row, text=avg["TAT"], width=10, fg="blue").pack(side="left")
#     tk.Label(avg_row, text=avg["RT"], width=10, fg="blue").pack(side="left")


# def show_comparison(rr_metrics, srtf_metrics):
#     for widget in table_frame.winfo_children():
#         widget.destroy()

#     show_table(table_frame, "Round Robin Results", rr_metrics)
#     show_table(table_frame, "SRTF Results", srtf_metrics)

#     rr_wt = rr_metrics["AVERAGE"]["WT"]
#     srtf_wt = srtf_metrics["AVERAGE"]["WT"]

#     if rr_wt < srtf_wt:
#         better = "Round Robin"
#     elif srtf_wt < rr_wt:
#         better = "SRTF"
#     else:
#         better = "Equal"

#     tk.Label(table_frame,
#              text=f"\nBetter Algorithm: {better}",
#              font=("Arial", 12, "bold"),
#              fg="green").pack()



# def run():
#     processes = build_processes()
#     if processes is None:
#         return

#     try:
#         quantum = int(quantum_entry.get())
#         if quantum < 1 or quantum > 100:
#             messagebox.showerror("Error", "Quantum must be between 1 and 100")
#             return
#     except ValueError:
#         messagebox.showerror("Error", "Invalid Quantum")
#         return

#     rr_processes = deepcopy(processes)
#     srtf_processes = deepcopy(processes)

#     rr_gantt, rr_queue, rr_metrics = round_robin(rr_processes, quantum)

   
#     try:
#         srtf_gantt, _, srtf_metrics = srtf(srtf_processes)
#     except:
#         srtf_gantt, _ = srtf(srtf_processes)
#         srtf_metrics = calculate_metrics(srtf_processes)

  
#     canvas.delete("all")
#     draw_gantt(rr_gantt, 0, "Round Robin")
#     draw_gantt(srtf_gantt, 120, "SRTF")

#     show_comparison(rr_metrics, srtf_metrics)


#     queue_text.delete("1.0", tk.END)
#     queue_text.insert(tk.END, "Ready Queue (RR):\n")
#     for q in rr_queue:
#         queue_text.insert(tk.END, str(q) + "\n")

  
#     output.delete("1.0", tk.END)
#     output.insert(tk.END, "RR Gantt:\n" + str(rr_gantt) + "\n\n")
#     output.insert(tk.END, "SRTF Gantt:\n" + str(srtf_gantt) + "\n")



# def create_inputs():
#     global arrival_entries, burst_entries, id_entries

#     for widget in inputs_frame.winfo_children():
#         widget.destroy()

#     arrival_entries = []
#     burst_entries = []
#     id_entries = []

#     try:
#         n = int(num_entry.get())
#     except ValueError:
#         messagebox.showerror("Error", "Enter valid number of processes")
#         return

#     for i in range(n):
#         tk.Label(inputs_frame, text="ID").grid(row=i, column=0)
#         pid = tk.Entry(inputs_frame)
#         pid.grid(row=i, column=1)

#         tk.Label(inputs_frame, text="Arrival").grid(row=i, column=2)
#         a = tk.Entry(inputs_frame)
#         a.grid(row=i, column=3)

#         tk.Label(inputs_frame, text="Burst").grid(row=i, column=4)
#         b = tk.Entry(inputs_frame)
#         b.grid(row=i, column=5)

#         id_entries.append(pid)
#         arrival_entries.append(a)
#         burst_entries.append(b)



# root = tk.Tk()
# root.title("CPU Scheduling")
# root.geometry("1000x750")

# tk.Label(root, text="Number of Processes").pack()
# num_entry = tk.Entry(root)
# num_entry.pack()

# tk.Label(root, text="Time Quantum").pack()
# quantum_entry = tk.Entry(root)
# quantum_entry.pack()

# inputs_frame = tk.Frame(root)
# inputs_frame.pack(pady=10)

# # Canvas + Scrollbars
# canvas_frame = tk.Frame(root)
# canvas_frame.pack()

# canvas = tk.Canvas(canvas_frame, width=900, height=200, bg="white")

# scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
# scroll_y_canvas = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

# canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y_canvas.set)

# canvas.pack(side="left", fill="both", expand=True)
# scroll_y_canvas.pack(side="right", fill="y")
# scroll_x.pack(fill="x")

# # Table
# table_frame = tk.Frame(root)
# table_frame.pack(pady=10)

# # Queue
# queue_text = tk.Text(root, height=6, width=50)
# queue_text.pack()

# # Buttons
# tk.Button(root, text="Create Inputs", command=create_inputs).pack(pady=5)
# tk.Button(root, text="Run", command=run).pack(pady=5)

# # Output
# output_frame = tk.Frame(root)
# output_frame.pack()

# output = tk.Text(output_frame, height=10, width=110)
# scroll_y = tk.Scrollbar(output_frame, command=output.yview)

# output.configure(yscrollcommand=scroll_y.set)

# output.pack(side="left")
# scroll_y.pack(side="right", fill="y")

# root.mainloop()
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from rr2 import round_robin
from srtf import srtf

# ===================== METRICS =====================

def calculate_metrics(processes):
    metrics = {}
    total_wt = total_tat = total_rt = 0
    n = len(processes)

    for p in processes:
        tat = p["completion"] - p["arrival"]
        wt = tat - p["burst"]
        rt = p["start"] - p["arrival"]

        metrics[p["id"]] = {
            "WT": wt,
            "TAT": tat,
            "RT": rt
        }

        total_wt += wt
        total_tat += tat
        total_rt += rt

    metrics["AVERAGE"] = {
        "WT": total_wt / n,
        "TAT": total_tat / n,
        "RT": total_rt / n
    }

    return metrics


# ===================== PROCESS BUILDER =====================

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
                messagebox.showerror("Error", f"Burst time must be positive")
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


# ===================== GANTT =====================

def draw_gantt(gantt, y_offset=0, title=""):
    canvas.create_text(50, 10 + y_offset, text=title, anchor="w", font=("Arial", 10, "bold"))

    if not gantt:
        return

    x = 10
    scale = 30

    for p, start, end in gantt:
        width = (end - start) * scale

        canvas.create_rectangle(x, 30 + y_offset, x + width, 80 + y_offset, fill="lightblue")
        canvas.create_text(x + width / 2, 55 + y_offset, text=p)

        canvas.create_text(x, 90 + y_offset, text=start)

        x += width + 10

    canvas.create_text(x, 90 + y_offset, text=gantt[-1][2])
    canvas.configure(scrollregion=canvas.bbox("all"))


# ===================== TABLE =====================

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

    avg = metrics["AVERAGE"]

    avg_row = tk.Frame(frame)
    avg_row.pack(pady=5)

    tk.Label(avg_row, text="AVG", width=10, fg="blue").pack(side="left")
    tk.Label(avg_row, text=avg["WT"], width=10, fg="blue").pack(side="left")
    tk.Label(avg_row, text=avg["TAT"], width=10, fg="blue").pack(side="left")
    tk.Label(avg_row, text=avg["RT"], width=10, fg="blue").pack(side="left")


# ===================== COMPARISON =====================

def show_comparison(rr_metrics, srtf_metrics):
    for widget in table_frame.winfo_children():
        widget.destroy()

    show_table(table_frame, "Round Robin Results", rr_metrics)
    show_table(table_frame, "SRTF Results", srtf_metrics)

    rr_wt = rr_metrics["AVERAGE"]["WT"]
    srtf_wt = srtf_metrics["AVERAGE"]["WT"]

    if rr_wt < srtf_wt:
        better = "Round Robin"
    elif srtf_wt < rr_wt:
        better = "SRTF"
    else:
        better = "Equal"

    tk.Label(table_frame,
             text=f"\nBetter Algorithm: {better}",
             font=("Arial", 12, "bold"),
             fg="green").pack()


# ===================== RUN =====================

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

    try:
        srtf_gantt, _, srtf_metrics = srtf(srtf_processes)
    except:
        srtf_gantt, _ = srtf(srtf_processes)
        srtf_metrics = calculate_metrics(srtf_processes)

    canvas.delete("all")
    draw_gantt(rr_gantt, 0, "Round Robin")
    draw_gantt(srtf_gantt, 120, "SRTF")

    show_comparison(rr_metrics, srtf_metrics)

    queue_text.delete("1.0", tk.END)
    queue_text.insert(tk.END, "Ready Queue (RR):\n")
    for q in rr_queue:
        queue_text.insert(tk.END, str(q) + "\n")

    output.delete("1.0", tk.END)
    output.insert(tk.END, "RR Gantt:\n" + str(rr_gantt) + "\n\n")
    output.insert(tk.END, "SRTF Gantt:\n" + str(srtf_gantt) + "\n")


# ===================== INPUTS =====================

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
        tk.Label(inputs_frame, text="ID").grid(row=i, column=0)
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


# ===================== GUI WITH SCROLLBAR =====================

root = tk.Tk()
root.title("CPU Scheduling")
root.geometry("1000x750")

# ===== SCROLLABLE MAIN CONTAINER =====
main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True)

canvas_main = tk.Canvas(main_container)
scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas_main.yview)

scrollbar.pack(side="right", fill="y")
canvas_main.pack(side="left", fill="both", expand=True)

canvas_main.configure(yscrollcommand=scrollbar.set)

main_frame = tk.Frame(canvas_main)
canvas_main.create_window((0, 0), window=main_frame, anchor="nw")


def on_configure(event):
    canvas_main.configure(scrollregion=canvas_main.bbox("all"))

main_frame.bind("<Configure>", on_configure)


# ===================== UI INSIDE MAIN FRAME =====================

tk.Label(main_frame, text="Number of Processes").pack()
num_entry = tk.Entry(main_frame)
num_entry.pack()

tk.Label(main_frame, text="Time Quantum").pack()
quantum_entry = tk.Entry(main_frame)
quantum_entry.pack()

inputs_frame = tk.Frame(main_frame)
inputs_frame.pack(pady=10)

# Canvas for Gantt
canvas_frame = tk.Frame(main_frame)
canvas_frame.pack()

canvas = tk.Canvas(canvas_frame, width=900, height=200, bg="white")
scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
scroll_y_canvas = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y_canvas.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y_canvas.pack(side="right", fill="y")
scroll_x.pack(fill="x")

# Table
table_frame = tk.Frame(main_frame)
table_frame.pack(pady=10)

# Queue
queue_text = tk.Text(main_frame, height=6, width=50)
queue_text.pack()

# Buttons
tk.Button(main_frame, text="Create Inputs", command=create_inputs).pack(pady=5)
tk.Button(main_frame, text="Run", command=run).pack(pady=5)

# Output
output_frame = tk.Frame(main_frame)
output_frame.pack()

output = tk.Text(output_frame, height=10, width=110)
scroll_y = tk.Scrollbar(output_frame, command=output.yview)

output.configure(yscrollcommand=scroll_y.set)

output.pack(side="left")
scroll_y.pack(side="right", fill="y")

root.mainloop()