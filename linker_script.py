#!/usr/bin/python

class LinkerScript:
    def __init__(self):
        self.symbols = []
        self.memories = []
        self.entry_point = None

    def add_symbol(self, name, address):
        self.symbols.append((name, address))

    def add_memory(self, name, address, size, permission):
        self.memories.append((name, address, size, permission))

    def set_entry_point(self, name, address):
        self.entry_point = (name, address)

    def __str__(self):
        ld = ''

        if self.entry_point != None:
            ld += '%s = 0x%08x;\nENTRY(%s)\n\n' % (self.entry_point[0], self.entry_point[1], self.entry_point[0])

        if len(self.memories) != 0x0:
            ld += 'MEMORY\n{\n'
            for name, address, size, permission in self.memories:
                if type(size) == int:
                    size = '%d' % size
                ld += '  %s (%s) : ORIGIN = 0x%08x, LENGTH = %s\n' % (name, permission, address, size)
            ld += '}\n\n'

        if len(self.symbols) != 0x0:
            ld += 'SECTIONS\n{\n'
            for name, address in self.symbols:
                ld += '  .%s 0x%08x : { *(.%s) }\n' % (name, address, name)
            #ld += '/DISCARD/ : { }\n'
            ld += '}\n\n'

        return ld

if __name__ == '__main__':
    lksc = LinkerScript()

    lksc.add_symbol('test', 0x4000)
    lksc.add_memory('ROM', 0x00000000, 0x00001000, 'rx')
    lksc.add_memory('RAM', 0x10000000, '256k', 'rw')
    lksc.add_symbol('TEST', 0x4000)
    lksc.set_entry_point('reset', 0x00000000)

    print(lksc)
