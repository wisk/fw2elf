#!/usr/bin/python

from elf_generator import ELFGenerator
from argparse import ArgumentParser
from sys import argv

from linker_script import LinkerScript

def get_entry_point(fw_path):
    return unpack('II', open(fw_path, 'rb').read(8))[1]

def main():
    target = 'cortex-m3'

    fw_input = None
    elf_output = None
    entry_point = None
    map_address = None
    target_name = 'cortex-m7'
    irq_no = 0

    parser = ArgumentParser(description='Firmware to ELF')
    parser.add_argument('-fw', '--firmware', required=True, help='Firmware file to convert to ELF')
    parser.add_argument('-e', '--elf', required=True, help='Converted ELF file')
    parser.add_argument('--target', help='Name of the target')
    parser.add_argument('--map-address', type=int, help='Address where the firmware is loaded')
    parser.add_argument('--entry-point', type=int, help='Address of reset handler')
    parser.add_argument('--irq-no', type=int, help='Number of IRQ')
    args = parser.parse_args(argv[1:])
    fw_input = args.firmware
    elf_output = args.elf
    entry_point = args.entry_point
    map_address = args.map_address
    #target_name = args.target_name
    irq_no = args.irq_no

    elf = ELFGenerator(fw_input, target_name, map_address, irq_no)
    elf.generate(elf_output)

if __name__ == '__main__':
    main()
