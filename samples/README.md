# Simple Samples

This directory holds a collection of samples for doing simple tests on the Pipistrello board using the ARTIQ environment.

NOTE: `device_db.pyon` is configured for use with the Pipistrello board. Make sure you edit this file when using a different device.

## How to Run Experiments

1. Following the instructions [here](https://m-labs.hk/artiq/manual-release-2/installing.html#installing-artiq) to create the environment for ARTIQ, while calling it `artiq-main`
2. Start your ARTIQ environment with `source activate artiq-main`
3. Run the following command to create a connection to the Pipistrello board
```sudo pppd /dev/ttyUSB1 115200 noauth nodetach local nocrtscts novj 10.0.0.1:10.0.0.2```
4. Run your experiments with `artiq_run your-experiment.py`
5. Use the GUI to run your experiments by running `artiq_master` in one terminal window, and `artiq_dashboard` in another window. Note that the current directory must have a `device_db.pyon` file and a `repository/` directory to hold experiments. This step may also take a few moments to run.
6. If changes are made to the experiment, run the command `artiq_client scan-repository` to refresh the GUI

## Output Mappings

The ARTIQ framework allows us to perform inputs and outputs through TTL. Below is a mapping of all TTL output lines to their corresponding ports on the Pipistrello LX45 FPGA board.

| `TTL` | `Channel:Port` |
|-------|----------------|
| TTL0  | C:11           |
| TTL1  | C:10           |
| TTL2  | C:9            |
| TTL3  | C:8            |
| TTL4  | C:7            |
| TTL5  | C:6            |
| TTL6  | C:5            |
| TTL7  | C:4            |
| TTL8  | C:3            |
| TTL9  | C:2            |
| TTL10 | C:1            |
| TTL11 | C:0            |
| TTL12 | B:4            |
| TTL13 | A:11           |
| TTL14 | B:5            |
| TTL15 | B:8            |