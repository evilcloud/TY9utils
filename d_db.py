import d_dict
import d_rig
import d_nvidia
from deta import Deta
import os
from dotenv import load_dotenv

load_dotenv()

DETA_KEY = os.environ["DETA_KEY"]


deta = Deta(DETA_KEY)

GPU_DB = deta.Base("GPUS")
RIG_DB = deta.Base("RIGS")

rig_content, cu = d_rig.get_rig_data()
gpu_content = d_nvidia.get_gpus_data()
rig = d_dict.add_to_rig({}, rig_content)
gpus = d_dict.add_to_gpu({}, gpu_content)
rig = d_dict.add_gpu_to_rig(rig, gpus)
gpus = d_dict.add_cu_to_gpu(gpus, cu)
for gpu in gpus:
    gpus[gpu]["rig"] = rig["name"]

for gpu in gpus:
    gpu_dict = gpus[gpu]
    gpu_dict["key"] = gpu
    GPU_DB.put(gpu_dict)

RIG_DB.put(rig)
