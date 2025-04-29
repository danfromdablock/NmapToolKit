# Nmap Scanner

**Advanced Nmap Scanner Script**

A Python wrapper for Nmap that supports both interactive and command-line modes, custom scan types, NSE scripts, host discovery options, decoys, and multiple output formats.

---

## Features

- **Target Flexibility**: Accepts IP addresses, hostnames, or URLs (automatically strips `http://`, `https://`, and `www.`).  
- **Interactive Mode**: Walks you through scan configuration without external dependencies.  
- **Customizable Scans**:  
  - TCP SYN, TCP Connect, and UDP scans  
  - Service version detection  
  - OS fingerprinting  
  - Default or custom NSE scripts (by category or file)  
  - Skip host discovery (`-Pn`)  
  - Decoy support  
- **Timing Control**: Choose Nmap timing templates (0–5).  
- **Port Ranges**: Specify port ranges (e.g., `1-65535`).  
- **Output Formats**: Normal (`-oN`), XML (`-oX`), Grepable (`-oG`), JSON (`-oJ`).  

---

## Prerequisites

- Python 3.6+ (tested on 3.8–3.12)  
- Nmap installed and available in your PATH  
- Root or sudo privileges for certain scan types  

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/danfromdablock/nmap-scanner.git
   cd nmap-scanner
