# Wireless Train Signalization Project

## Overview
This project is developed as part of the Bilkent University Electrical and Electronics Engineering Industrial Design Project. It aims to introduce a wireless railway signalization system utilizing RF-based wireless technologies and passive RFID antenna balises. This system is designed to optimize track capacity and safety by providing continuous communication and real-time management of train movements.

## Team Members
- Efe Tarhan
- Özge Özmısır
- Gökay Balcı
- Ege Yüceel
- Muhammed Berk Alemdar
- Mehmet Rıfat Özkurt

### Academic Mentor
- Prof. Ayhan Altıntaş

### Company Mentor
- Can Ali Yarman

### Teaching Assistant
- Elif Ahsen Çakmakci

## Project Summary
Savronik, founded in 1986 to serve the Turkish Defense Industry, has been working since its establishment to meet the product and system requirements of our defense industry using domestic resources to the maximum extent possible while addressing the current needs of the user authority with original solutions.

## Contents
1. [Motivation and Novelty](#motivation-and-novelty)
2. [Requirements](#requirements)
   - Functional Requirements
   - Non-Functional Requirements/Constraints
3. [Big Picture](#big-picture)
4. [Methods and Implementation Details](#methods-and-implementation-details)
5. [Results, Discussions, and Future Directions](#results-discussions-and-future-directions)
6. [Detailed Equipment List](#detailed-equipment-list)
7. [References](#references)

## Motivation and Novelty
- **Problem at Hand**: Rising traffic demand, security of energy supply, increasing population, and climate change are some of the major issues of today’s world.
- **Utilisation of the Project by Savronik A.Ş.**: To address these issues, the project introduces a wireless railway signalization system that utilizes RF-based wireless technologies and passive RFID antenna balises.

## Requirements
### Functional Requirements
1. Onboard device capable of radio-frequency communication with on-track RFID balises and centralized data center.
2. Periodic communication with data center to report expedition information.
3. Balises to transmit identity and error detection code to passing train.
4. Onboard transceivers to receive transmitted messages while in motion.
5. Unique ID for each onboard device.
6. Train identity assigned to onboard devices upon expedition initialization.
7. Onboard devices to broadcast GPS coordinates, latest checkpoint passed, and identity periodically.
8. Comparison of GPS coordinates measured by onboard device with absolute GPS coordinates of on-track transmitters.
9. Remote server to store all messages received from onboard devices.
10. Server-side collision detection software to check for any trains on the same track violating railway security regulations.
11. Signalization system to accurately detect and alert personnel about potential collisions.

### Non-Functional Requirements/Constraints
1. **Cost**: Complete system with two onboard devices, 10 on-track transceivers, and a remote server not to exceed 40,000 TL.
2. **Train Speed**: Onboard device to read data from on-track transceivers while moving at 80 km/h.
3. **Onboard Device Range**: Read on-track transceiver ID data from a minimum horizontal distance of 1 to 3 m.
4. **Size and Weight**: Maximum allowable size of 0.25 x 0.25 x 0.1 m and weight of 500 g.
5. **Power Consumption**: Power consumption below 5 watts and a current draw under 500 mA.
6. **Safety**: Compliance with system reliance, regulatory compliance, and data security standards.

## Big Picture
The system is composed of three main subsystems:
1. Onboard device
2. Online database and broker system
3. Graphical User Interface (GUI)

## Methods and Implementation Details
The project is divided into two subsystems: hardware and software.
- **Hardware**: Development boards, RFID components, GPS and WiFi modules.
- **Software**: Database design, GUI, and signalization algorithms.

## Results, Discussions, and Future Directions
### Results
The system successfully:
- Transmits critical information about trains.
- Receives and propagates GPS information.
- Detects potential collisions and raises alerts.
- Ensures data security and integrity.

### Discussions and Lessons Learned
- Emphasis on selecting the right components.
- Improvement needed in system waterproofing and RFID reader accuracy at high speeds.
- Better material selection and higher quality components recommended for future work.

## Detailed Equipment List
- RFID Readers
- Antennas
- Development Boards
- GPS Modules
- WiFi Modules
- RFID Tags
- Casing and Connectors

## References
- Turkish Standards Institute
- Ministry of Transport and Infrastructure
