import d_sys


# CONSTS #####

SAMPLE_GPU_FILE = "ng.out"
SAMPLE_PROC_FILE = "np.out"

NVIDIA_GPU_USED = (
    "index",
    "uuid",
    "name",
    "utilization.gpu",
    "utilization.memory",
    "power.draw",
    "pstate",
    "driver_version",
    "memory.total",
)
NVIDIA_GPU_UNUSED = (
    "gpu_serial",
    "display_active",
    "display_mode",
)
NVIDIA_GPU_QUERY = "query-gpu"

NVIDIA_PROC_USED = ("gpu_uuid", "pid", "process_name", "used_memory")
NVIDIA_PROC_UNUSED = ("gpu_serial", "gpu_bus_id", "gpu_board_id", "gpu_name")
NVIDIA_PROC_QUERY = "query-compute-apps"


# GPU #####


def get_nvidia_smi(bashparam: str, variables: list[str]):
    """
    Get nvidia smi
    :param bashparam: bash parameter
    :param variables: variables
    :return: nvidia smi output
    """
    # Get nvidia smi
    cmd = (
        f"nvidia-smi --{bashparam}={','.join(variables)} --format=csv,noheader,nounits"
    )
    output, err = d_sys.get_subprocess(cmd)
    return (output, err)


def merge_lists_to_dict(keys: list[str], values: list[str]) -> dict:
    """
    Merge lists to dict
    :param keys: list of keys
    :param values: list of values
    :return: merged dict
    """

    return dict(zip(keys, values))


def get_gpus_data() -> dict:
    """
    It runs `nvidia-smi` twice, once for the GPU data and once for the process data, and then merges the
    two together
    :return: A dictionary of dictionary of GPU data.
    """
    if d_sys.is_nvidia():
        out_gpu, err_gpu = get_nvidia_smi(NVIDIA_GPU_QUERY, NVIDIA_GPU_USED)
        out_proc, err_proc = get_nvidia_smi(NVIDIA_PROC_QUERY, NVIDIA_PROC_USED)
    else:
        out_gpu, err_gpu = d_sys.open_file(SAMPLE_GPU_FILE).splitlines(), False
        out_proc, err_proc = d_sys.open_file(SAMPLE_PROC_FILE).splitlines(), False
    if err_gpu or err_proc:
        print("Failed to get NVIDIA data")
        return ({}, True)
    gpus = [merge_lists_to_dict(NVIDIA_GPU_USED, gpu.split(", ")) for gpu in out_gpu]
    procs = [
        merge_lists_to_dict(NVIDIA_PROC_USED, proc.split(", ")) for proc in out_proc
    ]
    ret = {}
    # for gpu in gpus:
    #     ret[gpu["uuid"]] = gpu
    ret = {gpu["uuid"]: gpu for gpu in gpus}
    for proc in procs:
        ret[proc["gpu_uuid"]] |= proc
        del ret[proc["gpu_uuid"]]["gpu_uuid"]
    # for key, value in ret.items():
    #     ret[key] = d_sys.prettify(value, key)
    return (ret, False)


# MAIN ####


def main():
    gpu_aggregate, _ = get_gpus_data()

    for gpu in gpu_aggregate:
        print(gpu_aggregate[gpu])


if __name__ == "__main__":
    main()
