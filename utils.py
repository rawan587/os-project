# def calculate_metrics(processes):
#     result = {}
#     total_wt = 0
#     total_tat = 0
#     total_rt = 0

#     for p in processes:
#         tat = p["completion"] - p["arrival"]
#         wt = tat - p["burst"]
#         rt = p["start"] - p["arrival"]

#         result[p["id"]] = {
#             "WT": wt,
#             "TAT": tat,
#             "RT": rt,
#             "Arrival": p["arrival"],
#             "Burst": p["burst"],
#             "Completion": p["completion"],
#             "Start": p["start"]
#         }

#         total_wt += wt
#         total_tat += tat
#         total_rt += rt

#     n = len(processes)

#     result["AVERAGE"] = {
#         "WT": round(total_wt / n, 2),
#         "TAT": round(total_tat / n, 2),
#         "RT": round(total_rt / n, 2)
#     }

#     return result


# def reset_processes(processes):
#     for p in processes:
#         p["remaining"] = p["burst"]
#         p["start"] = -1
#         p["completion"] = 0


# def format_gantt(gantt):
#     return " | ".join([f"{p} ({s}-{e})" for p, s, e in gantt])


# def clone_processes(processes):
#     return [
#         {
#             "id": p["id"],
#             "arrival": p["arrival"],
#             "burst": p["burst"],
#             "remaining": p["burst"],
#             "start": -1,
#             "completion": 0
#         }
#         for p in processes
#     ]
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
            "RT": rt
        }

        total_wt += wt
        total_tat += tat
        total_rt += rt

    n = len(processes)

    avg_wt = round(total_wt / n, 2)
    avg_tat = round(total_tat / n, 2)
    avg_rt = round(total_rt / n, 2)

    result["AVERAGE"] = {
        "WT": avg_wt,
        "TAT": avg_tat,
        "RT": avg_rt
    }

    return result


def save_results_to_file(metrics, filename="results.txt"):
    with open(filename, "w") as file:
        file.write("=== Process Metrics ===\n\n")

        for pid, data in metrics.items():
            if pid == "AVERAGE":
                continue

            file.write(f"{pid}:\n")
            file.write(f"  WT = {data['WT']}\n")
            file.write(f"  TAT = {data['TAT']}\n")
            file.write(f"  RT = {data['RT']}\n\n")

        file.write("=== AVERAGES ===\n")
        file.write(f"Average WT  = {metrics['AVERAGE']['WT']}\n")
        file.write(f"Average TAT = {metrics['AVERAGE']['TAT']}\n")
        file.write(f"Average RT  = {metrics['AVERAGE']['RT']}\n")


# مثال استخدام:
processes = [
    {"id": "P1", "arrival": 0, "burst": 5, "start": 0, "completion": 10},
    {"id": "P2", "arrival": 1, "burst": 3, "start": 2, "completion": 8},
]

metrics = calculate_metrics(processes)

# طباعة في الكونسول
print(metrics)

# حفظ في ملف
save_results_to_file(metrics)