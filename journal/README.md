# Journal Entries

### Tasks

* Checkout datasets and applets within the GUI, following the instructions [here](https://m-labs.hk/artiq/manual-release-2/getting_started_mgmt.html#datasets) (Wed)
* Finish initialization and fix bugs with Pipistrello abstraction
* Create an easy way to setup the environment for ARTIQ and running code (a single executable package, instead of activating the source by hand and opening four separate terminals to run code).

## Mon Oct 31 🎃

* Moved to a 'kernel based' system for responding to input events. Currently, the kernel that gets executed on rising edge detection simply prints to the console, but this week will focus on incorporating more interesting procedures into the abstraction.


## Wed Oct 26

* Succesfully received input in the form of a "rising edge"; the board generates a signal with 10 rising edges from `TTL1`, which is channeled to `PMT0`, which reads the number of rising edges and prints the count. This experiment is located in the repo as `InputTest` in `input-test.py`. We can now use this for, say, detecting a rising edge from a device such as a single photon detector.
* Updated the `device_db.pyon` file to include input channels `PMT0` and `PMT1`
* Possible issue: it seems as though the NIST QC1 only has two input ports.

### Wed Oct 19

* Tested the TTL outputs and created a mapping of all TTL lines to ports on the bound, which can be found within the [samples folder](https://github.com/vontell/artiq-control/tree/master/samples).
* Configured `device_db.pyon` with another TTL output (TTL15)
* Configuration finished for `device_db.pyon` (besides PMT and DDS config)

### Mon Oct 17

* Determined the lower bound on the Pipistrello speed; UnderflowErrors are common around pulses of length 1 microsecond, and are always apparent at pulses of under 1 microsecond.
* Using the email correspondence [here](https://ssl.serverraum.org/lists-archive/artiq/2016-October/001022.html), and the TTL mappings [here](https://github.com/m-labs/artiq/blob/master/artiq/gateware/nist_qc1.py#L4), the Pipistrello board is finally putting out a signal as expected. Testing has been done on TTL0, generating the following square wave:
![alt text](https://i.imgur.com/jwL8DKM.jpg "Logo Title Text 1")

### Fri Oct 07

* Started to test TTL outputs on oscilliscope (needs further testing with assistance)

### Thu Oct 06

* Created `pulse-test.py`, which simply flashes LEDs on the board in order to test the connection.
* Configured TTL outputs within `device_db.pyon`

### Wed Oct 05

* LED and TTL outputs working on Pipistrello board
* `device_db.pyon` file partially configured
* Ran first experiment

### Mon Oct 03

* Liesure reading and studying on the [Barrett and Kok Protocol](http://journals.aps.org/pra/pdf/10.1103/PhysRevA.71.060310), along with [this paper](https://openaccess.leidenuniv.nl/bitstream/handle/1887/43200/Thesis%20Jacob%20Bakermans.pdf?sequence=1).

### Thu Sep 29

* ARTIQ can successfully count numbers using the experiment called `Count`, which is contained within the `simple-count.py` file.
* Learned that the experiment code can be refreshed using the command `artiq_client scan-repository` while active in the `(artiq-main)` environment

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
