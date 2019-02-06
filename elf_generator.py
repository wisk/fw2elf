#!/usr/bin/python

from subprocess import call
from sys import argv
from os import makedirs

from linker_script import LinkerScript
from cortex_m import CortexM


class ELFGenerator:
    BUILD_FOLDER = '__build/'
    C_SOURCE_FILE = BUILD_FOLDER + 'main.c'
    LD_SCRIPT_FILE = BUILD_FOLDER + 'tmp.ld'

    INITIAL_C_CODE = '''
typedef unsigned char u8_t;
typedef unsigned short u16_t;
typedef unsigned int u32_t;
typedef void (*handler_void_void_t)(void);
'''

    TYPE_TO_BYTE_SIZE = {
            'u8_t':1,
            'u16_t':2,
            'u32_t':4,
            'handler_void_void_t':4, # TODO: handle 64-bit arch
            }

    PREFIX = 'arm-none-eabi-'
    GCC = PREFIX + 'gcc'
    OBJCOPY = PREFIX + 'objcopy'

    def __init__(self, fw_path, target_name = None, map_address = None, irq_no = None):
        try:
            makedirs(ELFGenerator.BUILD_FOLDER)
        except FileExistsError:
            pass

        # TODO: figure out target from target name parameter
        self.target_name = target_name
        self.target = CortexM(7, map_address, irq_no)

        self.fw_path = fw_path
        map_address, stack_pointer, entry_point, irq_no = self.target.determine_information(self.fw_path)
        self.entry_point = entry_point

    def generate(self, elf_path):
        ld = LinkerScript()
        ld.set_entry_point('reset', self.entry_point)
        mmap = self.target.get_memory_map()
        syms = self.target.get_registers()

        for m in mmap:
            ld.add_memory(*m)
        for s in syms:
            ld.add_symbol(s[0], s[1])
        c_code = self._generate_c_file(syms)
        ld_script = str(ld)

        open(ELFGenerator.C_SOURCE_FILE, 'w').write(c_code)
        open(ELFGenerator.LD_SCRIPT_FILE, 'w').write(ld_script)

        self._compile_file(ELFGenerator.C_SOURCE_FILE, ELFGenerator.LD_SCRIPT_FILE, elf_path)
        self._update_section('.vt', self.fw_path, elf_path)

    def _generate_c_file(self, structures):
        c = ELFGenerator.INITIAL_C_CODE
        for s_name, s_address, s_members in structures:
            c += 'struct _%s {\n' % s_name
            current_address = s_address
            for m_name, m_type, m_address, m_description in sorted(s_members, key=lambda s: s[2]):
                # Handle padding here
                if current_address != m_address:
                    c += '  /* 0x%08x */  u8_t __padding__0x%08x_0x%08x[0x%08x];\n' % (current_address, current_address, m_address, m_address - current_address)
                    current_address = m_address

                c += '  /* 0x%08x */  %s %s; // %s\n' % (m_address, m_type, m_name, m_description)
                if not m_type in ELFGenerator.TYPE_TO_BYTE_SIZE:
                    raise Exception('Unknown type used: %s' % m_type)
                current_address += ELFGenerator.TYPE_TO_BYTE_SIZE[m_type]
            c += '} %s __attribute__((section(".%s")));\n' % (s_name.upper(), s_name)

        return c

    def _compile_file(self, source_file, link_script, elf_file):
        compiler = [ ELFGenerator.GCC ]
        cflags = [ '-ggdb3', '-nostdlib', '-nostartfiles', '-mcpu=%s' % self.target_name, '-mthumb' ]
        linker_script = [ link_script ]
        source_file = [ source_file ]
        output = [ '-o', elf_file ]
        call(compiler + cflags + linker_script + source_file + linker_script + output)

    def _update_section(self, section_name, raw_file, elf_file):
        objcopy = [ ELFGenerator.OBJCOPY ]
        objflags= [ '--update-section', '%s=%s' % (section_name, raw_file), elf_file ]
        call(objcopy + objflags)

if __name__ == '__main__':
    e = ELFGenerator(None)
    e.generate(None)
