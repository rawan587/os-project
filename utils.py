def calculate_metrics(processes):
    result = {}
    total_wt = 0
    total_tat = 0
    total_rt = 0

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


def reset_processes(processes):
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = -1
        p["completion"] = 0


def format_gantt(gantt):
    return " | ".join([f"{p} ({s}-{e})" for p, s, e in gantt])


def clone_processes(processes):
    return [
        {
            "id": p["id"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "remaining": p["burst"],
            "start": -1,
            "completion": 0
        }
        for p in processes
    ]