from datetime import timedelta
import json
import d_rig
import d_nvidia


class Rig:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def add_data(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def add_gpu(self, gpu: str):
        self.gpus.append(gpu)

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GPU:
    def add_data(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def add_cu(self, cu: float):
        self.cu = cu

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


rig_content, cu = d_rig.get_rig_data()
print(cu)
gpus_content = d_nvidia.get_gpus_data()
rig = Rig()
gpus = GPU()
for item in rig_content:
    print(item)

rig.add_data(rig_content)
gpus.add_data(gpus_content)
for item in gpus.__dict__:
    gpu = gpus.__dict__[item]
    print(gpu)
    print(item)
    rig.add_gpu(item)
    # if item == "cu":
    #     print(item)
    #     gpus.add_cu(item)
print(rig)
