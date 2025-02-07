TCP over UTP Implementation

📌 Overview
This project implements a TCP-like reliable file transfer protocol over UDP (UTP). The implementation ensures reliable data transmission between two PCs using Winsock2 and incorporates features such as Selective Repeat, ACK (Acknowledgment), NACK (Negative Acknowledgment), and error checking using CRC (Cyclic Redundancy Check).

✨ Features:
  - Reliable File Transfer – Ensures complete and accurate file transfer over an unreliable network using UDP.
  - Selective Repeat ARQ – Efficient retransmission mechanism to handle packet loss.
  - ACK & NACK Handling – Provides feedback on received and missing packets.
  - Error Checking (CRC) – Detects data corruption during transmission.
  - Winsock2-based Communication – Uses Windows socket API for network communication.

Header is represented as a struct and contains fields:
  - crc: u16
  - lengthL u16
  - sequence number: u16
  - type: enum DataTypes
  - window size: u16
  - isNextFragment: bool

Project includes a lua file for whireshark that allows to see the header fields
