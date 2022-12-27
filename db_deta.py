import collector

from deta import Deta
import os

# from dotenv import load_dotenv
# load_dotenv()

DETA_KEY = os.environ["DETA_KEY"]

deta = Deta(DETA_KEY)

GPU_DB = deta.Base("GPUS")
RIG_DB = deta.Base("RIGS")

gpus, rig = collector.get_gpus_rig()
for gpu in gpus:
    gpu_dict = gpus[gpu]
    gpu_dict["key"] = gpu
    GPU_DB.put(gpu_dict)

RIG_DB.put(rig)
