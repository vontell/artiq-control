# Journal Entries

### Tasks

* Configured `device_db.pyon` for thorough connection to the board
* Run first experiment on the board (simple LED experiments will suffice)
* Follow the steps [here](https://m-labs.hk/artiq/manual-release-2/getting_started_mgmt.html) to use the ARTIQ GUI!

### Wed Sep 28

* ARTIQ has been futher configured. I have successfully connected to the Pipistrello, and am making progress on configuring a `device_db.pyon` file for further testing that the board is actually connected. Current issues include finding the correct RTIO channel that corresponds to the LED on the board.
* An idle kernel has been flashed on the Pipistrello, which should turn the LED on and off every half second (although not tested as the `device_db.pyon` file needs to be configured correctly).
* More conversation can be found [here](https://github.com/m-labs/artiq/issues/568) from working out an issue with connecting to the FPGA board.

### Tue Sep 27

* ARTIQ and Ubuntu configured on desktop in lab. Pipistrello not yet connected.

### Mon Sep 26

* Found out that Mac does not support the flashing software for Pipistrello. Instead, the environment has been setup with Ubuntu.

### Wed Sep 21

* Setup most of the ARTIQ environment on OSX following the instructions [here](https://m-labs.hk/artiq/manual-release-2/installing_from_source.html#install-from-source).   
