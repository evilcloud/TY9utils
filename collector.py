from datetime import datetime, timedelta
import d_sys
import d_nvidia
import d_rig
import json

NVIDIA_GPU_MAPPING = {
    "manufacturer": "NVIDIA",
    "index": "index",
    "uuid": "uuid",
    "name": "model",
    "utilization.gpu": "gpu_util",
    "utilization.memory": "memory_util",
    "power.draw": "power_draw",
    "pstate": "pstate",
    "driver_version": "driver_version",
    "memory.total": "memory_total",
    "gpu_serial": "gpu_serial",
    "display_active": "display_active",
    "display_mode": "display_mode",
    "gpu_uuid": "gpu_uuid",
    "pid": "pid",
    "process_name": "process_name",
    "used_memory": "memory_used",
    "gpu_bus_id": "gpu_bus_id",
    "gpu_board_id": "gpu_board_id",
    "gpu_name": "gpu_name",
}


def remap_keys(data: dict, mapping: dict) -> dict:
    """
    Remap keys
    :param data: data
    :param mapping: mapping
    :return: remapped data
    """
    return {mapping[k]: v for k, v in data.items()}


def prettify(item: str, designation: str):
    match designation:
        case "cu" | "proc_id" | "index" | "power_draw" | "memory_total" | "pid" | "memory_used" | "memory_util" | "gpu_util":
            return d_sys.to_int(item)
        case "hashrate":
            return d_sys.to_float(item)
        # case "runtime":
        #     dt = datetime.strptime(item, "%H:%M")
        #     return timedelta(hours=dt.hour, minutes=dt.minute)
        case _:
            # print(item, designation)
            return item


def collect_nvidia():
    nvidia, err = d_nvidia.get_gpus_data()
    if err:
        return {}

    data = {}
    for gpu in nvidia:
        gpu = remap_keys(nvidia[gpu], NVIDIA_GPU_MAPPING)
        gpu = {key: prettify(value, key) for key, value in gpu.items()}
        data[gpu["uuid"]] = gpu
    return data


def collect_rig():
    rig, cu = d_rig.get_rig_data()
    rig = {key: prettify(value, key) for key, value in rig.items()}
    ncu = {prettify(cu, "cu"): prettify(hr, "hashrate") for cu, hr in cu.items()}
    return (rig, ncu)


def add_rig_to_gpu(gpus: dict, rig: dict, cu: dict):
    for gpu in gpus.values():
        index = gpu.get("index", None)
        gpu["rig"] = rig.get("name", "N/A")
        gpu["cu"] = cu.get(index, 0)
    return gpus


def add_gpu_to_rig(rig: dict, gpus: dict):
    for gpu in gpus.values():
        total_power_draw = gpu.get("total_power", 0)
    rig["total_power"] = total_power_draw
    return rig


def crosscontaminate_data():
    gpu = collect_nvidia()
    rig, cu = collect_rig()
    gpu = add_rig_to_gpu(gpu, rig, cu)
    rig = add_gpu_to_rig(rig, gpu)
    return (gpu, rig)


def get_gpus_rig():
    return crosscontaminate_data()


def main():
    gpus, rig = get_gpus_rig()
    print(json.dumps(rig, indent=4))
    print(json.dumps(gpu, indent=4))


if __name__ == "__main__":
    main()
