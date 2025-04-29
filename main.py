#!/usr/bin/env python3
"""
Advanced Nmap Scanner Script
- Supports IP/hostname or URL targets (auto-strips protocols)
- Interactive mode without external dependencies
- Select scan types, NSE scripts, host discovery, decoys
- Multiple output formats (normal, XML, grepable, JSON)

Usage Examples:
    # Run in interactive mode (prompts for all options):
    python3 nmap_scanner.py

    # Run a SYN scan against a URL target
    python3 nmap_scanner.py https://example.com -sS -T5 -oN results.txt

    # Full aggressive scan with all defaults
    sudo python3 nmap_scanner.py http://target.org -sS -sV -O -sC -T5 -oN full_scan.txt

    # Use specific NSE categories and skip ping
    python3 nmap_scanner.py www.example.com --script-cats vuln,discovery -Pn -T4 -oN vuln_scan.txt
"""
import argparse
import subprocess
import sys
import re


def strip_url(target: str) -> str:
    return re.sub(r'^(https?://)?(www\.)?', '', target)


def parse_args():
    parser = argparse.ArgumentParser(description='Advanced Nmap Scanner')
    parser.add_argument('target', nargs='?', help='IP, hostname, or URL (omit for interactive mode)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive prompts')
    parser.add_argument('-sS', '--syn-scan', action='store_true', help='TCP SYN scan')
    parser.add_argument('-sT', '--connect-scan', action='store_true', help='TCP Connect scan')
    parser.add_argument('-sU', '--udp-scan', action='store_true', help='UDP scan')
    parser.add_argument('-sV', '--version-detect', action='store_true', help='Service version detection')
    parser.add_argument('-sC', '--script-default', action='store_true', help='Default NSE scripts')
    parser.add_argument('--script-cats', help='Comma-separated NSE categories')
    parser.add_argument('--script-file', help='Specific NSE script or directory')
    parser.add_argument('-O', '--os-detect', action='store_true', help='OS detection')
    parser.add_argument('-Pn', '--skip-ping', action='store_true', help='Skip host discovery')
    parser.add_argument('--decoy', help='Comma-separated decoy IPs')
    parser.add_argument('-T', '--timing', type=int, choices=range(0,6), default=4, help='Timing (0-5)')
    parser.add_argument('-p', '--ports', help='Port range (e.g. 1-65535)')
    parser.add_argument('-oN', '--output-normal', help='Normal output file')
    parser.add_argument('-oX', '--output-xml', help='XML output file')
    parser.add_argument('-oG', '--output-grep', help='Grepable output file')
    parser.add_argument('-oJ', '--output-json', help='JSON output file')
    return parser.parse_args()


def build_command(cfg):
    cmd = ['sudo', 'nmap']
    if cfg.skip_ping: cmd.append('-Pn')
    if cfg.syn_scan: cmd.append('-sS')
    if cfg.connect_scan: cmd.append('-sT')
    if cfg.udp_scan: cmd.append('-sU')
    if cfg.version_detect: cmd.append('-sV')
    if cfg.script_default: cmd.append('-sC')
    if cfg.script_cats: cmd.extend(['--script', cfg.script_cats])
    if cfg.script_file: cmd.extend(['--script', cfg.script_file])
    if cfg.os_detect: cmd.append('-O')
    if cfg.decoy: cmd.extend(['--decoy', cfg.decoy])
    cmd.append(f'-T{cfg.timing}')
    if cfg.ports: cmd.extend(['-p', cfg.ports])
    cmd.append(cfg.target)
    if cfg.output_normal: cmd.extend(['-oN', cfg.output_normal])
    if cfg.output_xml: cmd.extend(['-oX', cfg.output_xml])
    if cfg.output_grep: cmd.extend(['-oG', cfg.output_grep])
    if cfg.output_json: cmd.extend(['-oJ', cfg.output_json])
    return cmd


def interactive_mode():
    print('--- Interactive Nmap Configuration ---')
    target = input('Target IP/hostname/URL: ').strip()
    target = strip_url(target)
    print('Select scans (comma separated): 1) SYN 2) Connect 3) UDP 4) Version 5) OS 6) Default scripts')
    choices = input('Enter numbers [1-6]: ').split(',')
    cfg = argparse.Namespace(**{k: False for k in vars(parse_args())})
    cfg.target = target
    cfg.skip_ping = input('Skip host discovery? (y/N): ').lower().startswith('y')
    cfg.syn_scan   = '1' in choices
    cfg.connect_scan = '2' in choices
    cfg.udp_scan   = '3' in choices
    cfg.version_detect = '4' in choices
    cfg.os_detect  = '5' in choices
    cfg.script_default = '6' in choices
    cfg.script_cats  = input('NSE categories (e.g. vuln,discovery) or leave blank: ').strip() or None
    cfg.script_file  = input('Specific NSE script file/dir or blank: ').strip() or None
    cfg.decoy       = input('Decoy IPs (comma separated) or blank: ').strip() or None
    cfg.timing      = int(input('Timing template (0-5) [4]: ') or 4)
    cfg.ports       = input('Port range [1-1000]: ').strip() or '1-1000'
    cfg.output_normal = input('Output file name [scan.txt]: ').strip() or 'scan.txt'
    cfg.output_xml  = None; cfg.output_grep = None; cfg.output_json = None
    return cfg


def main():
    args = parse_args()
    if args.interactive or not args.target:
        cfg = interactive_mode()
    else:
        args.target = strip_url(args.target)
        cfg = args
    cmd = build_command(cfg)
    print('Running:', ' '.join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print('Scan complete.')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == '__main__':
    main()
