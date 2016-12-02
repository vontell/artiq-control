# ARTIQ and Qubit Control (NV Centers)

[![Join the chat at https://gitter.im/artiq-control/Lobby](https://badges.gitter.im/artiq-control/Lobby.svg)](https://gitter.im/artiq-control/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a compilation of the notes and code from a UROP within the RLE at MIT with the Quantum Photonics Laboratory under Dirk Englund.

### Project Abstract
This project involves the configuration and use of ARTIQ, (Advanced Real-Time Infrastructure for Quantum physics), a control system for quantum information processing.  ARTIQ, at the highest level, is a set of FPGA and python code built to create a flexible control architecture for manipulating qubits.  The FPGA allows ARTIQ to take advantage of real-time parallel processing to control multiple qubits simultaneously. The project will involve configuring and testing ARTIQ to control qubits in the form of Nitrogen-Vacancy Centers (NV) in diamond. The FPGA will be producing TTL pulse sequences that will control various electromagnetic (EM) fields (microwave sources and visible lasers) that are resonant with relevant NV state transitions.  It will also be monitoring emitted photons (using an avalanche photodiode which detects single photons) to determine when the pulse sequence has been successful.  These pulse sequences will be used to initialize the qubits and to perform computations on these qubits, with a final goal of creating a quantum repeater. The project will be advised by Dirk Englund and Michael Walsh, within the Quantum Photonics Laboratory at the RLE.

### Environment Setup

The ARTIQ environment can be setup through the following guides. For users on a Windows and Linux machine, you can use the guide found [here](https://m-labs.hk/artiq/manual-release-2/installing.html#id2). For those on a OSX-based machine, install directly from source using the steps [here](https://m-labs.hk/artiq/manual-release-2/installing_from_source.html#install-from-source). More information on ARTIQ in general can also be found at [https://m-labs.hk/artiq/](https://m-labs.hk/artiq/).