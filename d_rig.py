import d_nvidia
import d_sys
from datetime import datetime

SAMPLE_MINING_FILE = "mining.out"
MINING_QUERY = "systemctl status abel.service"

# MINING ####


def get_mining_data() -> dict:
    mining_lines, err = d_sys.get_subprocess(MINING_QUERY)
    if err:
        print("Failed to get mining data. Loading sample data")
        mining_lines = d_sys.open_file(SAMPLE_MINING_FILE).splitlines()
    return mining_lines


def get_last_mining(lines):
    for line in lines[::-1]:
        if " m " in line:
            return line.split()


def parse_mining_line(line: str):
    rig_line = {
        "prog_datetime": " ".join([line[0], line[1], line[2]]),
        "current_datetime": str(datetime.now().timestamp()),
        "name": line[3],
        "key": line[3],
        "proc_name": line[4].split("[")[0],
        "proc_id": line[4].split("[")[1],
        "runtime": line[8],
        "hashrate": line[10],
        "hashratio": line[11],
    }
    for key, value in rig_line.items():
        rig_line[key] = d_sys.prettify(value, key)
    rig_line["hashrate"] = d_sys.prettify(rig_line["hashrate"], "hashrate")
    del rig_line["hashratio"]
    # cu_line = {
    #     d_sys.prettify(d_sys.to_int(cu), "cu"): d_sys.prettify(hr, "hashrate")
    #     for cu, hr in zip(line[13::2], line[14::2])
    # }
    cu_line = dict(zip(line[13::2], line[14::2]))
    return rig_line, cu_line


def get_rig_data() -> tuple:
    system = d_sys.get_system_info()
    rig = {
        "name": system["hostname"],
        "os": system["os_name"],
    }
    mining_data = get_mining_data()
    last_mint = get_last_mining(mining_data)
    parsed_line, parsed_cu = parse_mining_line(last_mint)
    rig |= parsed_line
    # for key, value in rig.items():
    #     rig[key] = d_sys.prettify(value, key)
    return rig, parsed_cu


def main():
    print(get_rig_data())


if __name__ == "__main__":
    main()
