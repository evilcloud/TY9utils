import socket
import platform
import subprocess
import shlex


def open_file(filename: str) -> str:
    """
    Open a file and return its contents as a string.
    """
    with open(filename, "r") as f:
        return f.read()


def get_system_info() -> dict:
    """
    Get system information
    :return: system info
    """
    return {
        "hostname": socket.gethostname(),
        "os_name": platform.system(),
        "os_version": platform.version(),
    }


def get_subprocess(cmd: str):
    """
    Get subprocess output

    Args:
        cmd (str): Command to execute
    """
    # Get subprocess output
    print(cmd)
    cmd = shlex.split(cmd)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = output.decode("utf-8").splitlines()
        return output, False
    except subprocess.CalledProcessError as err:
        return (err.output, True)
    except Exception as err:
        return (err, True)


def is_nvidia() -> bool:
    """
    Check if nvidia drivers are installed
    """
    try:
        subprocess.check_output("nvidia-smi")
        return True
    except Exception:
        print("No Nvidia GPU in system!")
        return False


def is_amd() -> bool:
    """
    Check if AMD drivers are installed
    :return: True if AMD drivers are installed
    """
    output, err = get_subprocess("aticonfig --odgt")
    return not err


def is_intel() -> bool:
    """
    Check if Intel drivers are installed
    :return: True if Intel drivers are installed
    """
    output, err = get_subprocess("icc --version")
    return not err


def to_float(value: str, precision: int = 2) -> float:
    """
    Convert string to float
    :param value: value to convert
    :param precision: precision
    :return: float
    """
    ret = "".join([i for i in str(value) if i.isdigit() or i == "."])
    try:
        return round(float(ret), precision)
    except Exception:
        print("Failed to convert to float")
        return 0


def to_int(value: str) -> int:
    return int(to_float(value))


def normalise_hashrate(value: str, ratio: str) -> float:
    ratio_dict = {
        "MH": 1,
        "KH": 1 / 1000,
        "H": 1 / 1000 / 1000,
        "GH": 1000,
    }
    return to_float(value) * ratio_dict[ratio.upper()]


def prettify(item: str, designation: str):
    match designation:
        case "cu" | "proc_id" | "index":
            return to_int(item)
        case "hashrate":
            return to_float(item)
        case _:
            return item
