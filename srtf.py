from copy import deepcopy

def srtf(processes):
    processes = deepcopy(processes)

    time = 0
    completed = 0
    n = len(processes)
    gantt = []

    while completed < n:
        ready = [p for p in processes if p["arrival"] <= time and p["remaining"] > 0]

        if not ready:
            future_arrivals = [p["arrival"] for p in processes if p["remaining"] > 0 and p["arrival"] > time]
            if future_arrivals:
                next_time = min(future_arrivals)
                gantt.append(("IDLE", time, next_time))
                time = next_time
            else:
                time += 1
            continue

        p = min(ready, key=lambda x: (x["remaining"], x["arrival"], x["id"]))

        if p["start"] == -1:
            p["start"] = time

        gantt.append((p["id"], time, time + 1))
        p["remaining"] -= 1
        time += 1

        if p["remaining"] == 0:
            p["completion"] = time
            completed += 1

    metrics = calculate_metrics(processes)
    return gantt, processes, metrics


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