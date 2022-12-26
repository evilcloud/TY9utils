from datetime import timedelta
import d_rig
import d_nvidia
import d_sys


def add_to_rig(rig: dict, data: dict):
    for key, value in data.items():
        rig[key] = value
    return rig


def add_gpu_to_rig(rig: dict, gpus: dict):
    rig["gpus"] = list(gpus)
    return rig


def add_to_gpu(gpu: dict, data: dict):
    for key, value in data.items():
        gpu[key] = value
    return gpu


def add_cu_to_gpu(gpus: dict, cu: dict):
    for gpu in gpus:
        gpus[gpu]["cu"] = cu[d_sys.to_int(gpus[gpu]["index"])]
    return gpus


rig_content, cu = d_rig.get_rig_data()
gpu_content = d_nvidia.get_gpus_data()
rig = add_to_rig({}, rig_content)
gpus = add_to_gpu({}, gpu_content)
rig = add_gpu_to_rig(rig, gpus)
gpus = add_cu_to_gpu(gpus, cu)
# gpus = {gpus[gpu]["rig"]: rig["name"] for gpu in gpus}
