from copy import deepcopy


def round_robin(processes, quantum):
    processes = deepcopy(processes)
    processes = sorted(processes, key=lambda x: (x["arrival"], x["id"]))

    time = 0
    queue = []
    gantt = []
    ready_queue_history = []   # ✅ مهم

    n = len(processes)
    i = 0
    completed = 0

    while completed < n:
        while i < n and processes[i]["arrival"] <= time:
            queue.append(processes[i])
            i += 1

        
        if not queue:
            next_time = processes[i]["arrival"] if i < n else time + 1

            
            if gantt and gantt[-1][0] == "IDLE":
                gantt[-1] = ("IDLE", gantt[-1][1], next_time)
            else:
                gantt.append(("IDLE", time, next_time))

            time = next_time
            continue

       
        ready_queue_history.append((time, [p["id"] for p in queue]))

        p = queue.pop(0)

        if p["start"] == -1:
            p["start"] = time

        exec_time = min(quantum, p["remaining"])

        
        if gantt and gantt[-1][0] == p["id"]:
            gantt[-1] = (p["id"], gantt[-1][1], gantt[-1][2] + exec_time)
        else:
            gantt.append((p["id"], time, time + exec_time))

        time += exec_time
        p["remaining"] -= exec_time

        
        while i < n and processes[i]["arrival"] <= time:
            queue.append(processes[i])
            i += 1

        if p["remaining"] > 0:
            queue.append(p)
        else:
            p["completion"] = time
            completed += 1

    metrics = calculate_metrics(processes)

    return gantt, ready_queue_history, metrics


def calculate_metrics(processes):
    result = {}
    total_wt = total_tat = total_rt = 0

    for p in processes:
        tat = p["completion"] - p["arrival"]
        wt = tat - p["burst"]
        rt = p["start"] - p["arrival"]

        result[p["id"]] = {
            "WT": wt,
            "TAT": tat,
            "RT": rt,
            "Arrival": p["arrival"],
            "Burst": p["burst"],
            "Completion": p["completion"],
            "Start": p["start"]
        }

        total_wt += wt
        total_tat += tat
        total_rt += rt

    n = len(processes)

    result["AVERAGE"] = {
        "WT": round(total_wt / n, 2),
        "TAT": round(total_tat / n, 2),
        "RT": round(total_rt / n, 2)
    }

    return result