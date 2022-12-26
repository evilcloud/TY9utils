# Reporting app -- general outline of functions and methods

## General required functions

### Capture and report

#### Continious

- System stats (CPU/Memory/etc)
- systemd processes
  - run.sh / abel
  - own process
- temperature
- GPU temperature

#### On boot

- hostname
- processor
- RAM
- GPUs
  - type
  - UID
  - serial number
  - power limit
- boot medium (usb.json)

## The process of caputring

### GPU

NVIDIA provides a well rounded utility `nvidia-smi` that allows to capture all necessary information about the GPUs

### systemd

`subprocess` with pipes

### system stats

`subprocess` or one of the utilities, depending on the target (Telegraf for InfluxDB for example)
