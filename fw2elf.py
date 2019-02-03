#!/usr/bin/python

from subprocess import call
from argparse import ArgumentParser
from struct import unpack
from sys import argv
from os import makedirs

LINKER_TEMPLATE = '''

reset = 0x%08x;
ENTRY(reset)

SECTIONS
{
        . = 0x%08x;
        .iv : { *(.iv) }
        . = 0xe000e000;
        .scs : { *(.scs) }
}
'''

BUILD_FOLDER = '__build/'
LINKER_SCRIPT = BUILD_FOLDER + 'tmp.ld'

PREFIX = 'arm-none-eabi-'
GCC = PREFIX + 'gcc'
OBJCOPY = PREFIX + 'objcopy'

def get_entry_point(fw_path):
    return unpack('II', open(fw_path, 'rb').read(8))[1]

def main():
    try:
        makedirs(BUILD_FOLDER)
    except FileExistsError:
        pass

    target = 'cortex-m3'

    fw_input = None
    elf_output = None
    entry_point = None
    map_address = None

    parser = ArgumentParser(description='Firmware to ELF')
    parser.add_argument('-fw', '--firmware', required=True, help='Firmware file to convert to ELF')
    parser.add_argument('-e', '--elf', required=True, help='Converted ELF file')
    parser.add_argument('--map-address', type=int, help='Address where the firmware is loaded')
    parser.add_argument('--entry-point', type=int, help='Address of reset handler')
    args = parser.parse_args(argv[1:])
    fw_input = args.firmware
    elf_output = args.elf
    entry_point = args.entry_point
    map_address = args.map_address

    if entry_point is None:
        entry_point = get_entry_point(fw_input)
    if map_address is None:
        map_address = entry_point & 0xffff0000

    print('Entry point: 0x%08x' % entry_point)
    print('Map address: 0x%08x' % map_address)

    open(LINKER_SCRIPT, 'w').write(LINKER_TEMPLATE % (entry_point, map_address))

    compiler = [ GCC ]
    cflags = [ '-shared', '-ggdb3', '-nostdlib', '-nostartfiles', '-mcpu=%s' % target, '-mthumb' ]
    linker_script = [ LINKER_SCRIPT ]
    source_file = [ target + '/main.c' ]
    output = [ '-o', elf_output ]
    call(compiler + cflags + linker_script + source_file + linker_script + output)


    objcopy = [ OBJCOPY ]
    objflags= [ '--update-section', '.iv=%s' % fw_input, elf_output ]
    call(objcopy + objflags)

if __name__ == '__main__':
    main()
