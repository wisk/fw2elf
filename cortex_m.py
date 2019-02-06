#!/usr/bin/python

from struct import unpack

class CortexM:
    def __init__(self, version, map_address = None, irq_no = None):
        self.version = version
        self.map_address = map_address
        self.irq_no = irq_no

    def determine_information(self, fw_path):
        fw_file = open(fw_path, 'rb')
        sp, reset = unpack('II', fw_file.read(8))

        fw_file.seek(0x40)
        irq_no = None
        map_address = reset & ~0x0000ffff
        for i in range(240): # max IRQ no + 1
            current_handler = unpack('I', fw_file.read(4))[0]
            if current_handler == 0x00000000:
                continue
            if current_handler & 0xff000000 != 0x00000000:
                irq_no = i
                break
            map_address &= current_handler
        print('MapAddress: 0x%08x, StackPointer: 0x%08x, ResetHandler: 0x%08x, IrqNumber: %d' % (map_address, sp, reset, irq_no))
        if self.map_address is None:
            self.map_address = map_address 
        if self.irq_no is None:
            self.irq_no = irq_no
        return map_address, sp, reset, irq_no


    def get_memory_map(self):
        return [
                ('Code',                 0x00000000, 0x20000000, 'rwx'),
                ('SRAM',                 0x20000000, 0x20000000, 'rwx'),
                ('Peripheral',           0x40000000, 0x20000000, 'rw' ),
                ('ExternalRAM',          0x60000000, 0x40000000, 'rwx'),
                ('ExternalDevice',       0xa0000000, 0x40000000, 'rw' ),
                ('PrivatePeripheralBus', 0xe0000000, 0x00100000, 'rw' ),
                ('VendorSpecificDevice', 0xe0100000, 0x1fff0000, 'rw' ),
                ]

    def get_registers(self):
        word = 'u32_t'
        handler = 'handler_void_void_t'

        vector_table = ('vt', self.map_address, [
            ('initial_sp'    , handler, self.map_address + 0x00, 'Initial Stack Pointer value'),
            ('reset'         , handler, self.map_address + 0x04, 'Reset handler'),
            ('nmi'           , handler, self.map_address + 0x08, 'Non-Maskable Interrupt handler'),
            ('hardfault'     , handler, self.map_address + 0x0c, 'Hard Fault handler'),
            ('mem_mgmt_fault', handler, self.map_address + 0x10, 'Memory Management Fault handler'),
            ('bus_fault'     , handler, self.map_address + 0x14, 'Bus Fault handler'),
            ('usage_fault'   , handler, self.map_address + 0x18, 'Usage Fault handler'),
            *( ('rsvd_%d' % i, handler, self.map_address + 0x1c + i * 4, 'Reserved interrupt handler %d' % i) for i in range(4) ),
            ('sv_call'       , handler, self.map_address + 0x2c, 'Supervisor Call handler'),
            ('dbg_rsvd'      , handler, self.map_address + 0x30, 'Reserved for Debug handler'),
            ('rsvd_4'        , handler, self.map_address + 0x34, 'Reserved interrupt handler 4'),
            ('pend_sv'       , handler, self.map_address + 0x38, 'Pending Supervisor Call handler'),
            ('systick'       , handler, self.map_address + 0x3c, 'System Tick handler'),
            *( ('irq%d' % i  , handler, self.map_address + 0x40 + i * 4, 'Interrupt Request %d' % i) for i in range(self.irq_no) ),
            ])


        private_peripheral_bus = ('ppb', 0xe000e000, [
                # System Control Block
                ('ACTLR', word, 0xe000e008, 'Auxiliary Control Register'),
                ('CPUID', word, 0xe000ed00, 'CPU identifier'),
                ('ICSR' , word, 0xe000ed04, 'Interrupt Control and State Register'),
                ('VTOR' , word, 0xe000ed08, 'Vector Table Offset Register'),
                ('AIRCR', word, 0xe000ed0c, 'Application Interrupt and Reset Control Register'),
                ('SCR'  , word, 0xe000ed10, 'System Control Register'),
                ('CCR'  , word, 0xe000ed14, 'Configuration and Control Register'),
                ('SHPR1', word, 0xe000ed18, 'System Handler Priority Register 1'),
                ('SHPR2', word, 0xe000ed1c, 'System Handler Priority Register 2'),
                ('SHPR3', word, 0xe000ed20, 'System Handler Priority Register 3'),
                ('SHCRS', word, 0xe000ed24, 'System Handler Control and State Register'),
                ('CFSR' , word, 0xe000ed28, 'Configurable Fault Status Register'),
                # TODO: handle union?
                ('HFSR' , word, 0xe000ed2c, 'HardFault Status Register'),
                ('MMAR' , word, 0xe000ed34, 'MemManage Fault Address Register'),
                ('BFAR' , word, 0xe000ed38, 'BusFault Address Register'),
                ('AFSR' , word, 0xe000ed3c, 'Auxiliary Fault Status Register'),

                # System Timer
                ('SYST_CSR'  , word, 0xe000e010, 'SysTick Control and Status Register'),
                ('SYST_RVR'  , word, 0xe000e014, 'SysTick Reload Value Register'),
                ('SYST_CVR'  , word, 0xe000e018, 'SysTick Current Value Register'),
                ('SYST_CALIB', word, 0xe000e01c, 'SysTick Calibration Value Register'),

                # Nested Vectored Interrupt Controller
                *( ('NVIC_ISER%d' % i, word, 0xe000e100 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range( 8) ),
                *( ('NVIC_ICER%d' % i, word, 0xe000e180 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range( 8) ),
                *( ('NVIC_ISPR%d' % i, word, 0xe000e200 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range( 8) ),
                *( ('NVIC_ICPR%d' % i, word, 0xe000e280 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range( 8) ),
                *( ('NVIC_IABR%d' % i, word, 0xe000e300 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range( 8) ),
                *( ('NVIC_IPR%d'  % i, word, 0xe000e400 + i * 4, 'Interrupt Set-enable Register %d' % i) for i in range(60) ),
                ('STIR', word, 0xe000ef00, 'Software Trigger Interrupt Register'),

                # Processor features
                ('CLIDR' , word, 0xe000ed78, 'Cache Level ID Register'),
                ('CTR'   , word, 0xe000ed7c, 'Cache Type Register'),
                ('CCSIDR', word, 0xe000ed80, 'Cache Size ID Register'),
                ('CSSELR', word, 0xe000ed84, 'Cache Size Selection Register'),

                # Memory Protection Unit
                ('MPU_TYPE', word, 0xe000ed90, 'MPU Type Register'),
                ('MPU_CTRL', word, 0xe000ed94, 'MPU Control Register'),
                ('MPU_RNR' , word, 0xe000ed98, 'MPU Region Number Register'),
                #('MPU_RBAR', word, 0xe000ed9c, 'MPU Region Base Address Register'),
                #('MPU_RASR', word, 0xe000eda0, 'MPU Region Attribute and Size Register'),
                *( ('MPU_RBAR_A%d' % i, word, 0xe000ed9c + i * 8, 'MPU Region Base Address Register %d' % i) for i in range(4) ),
                *( ('MPU_RASR_A%d' % i, word, 0xe000eda0 + i * 8, 'MPU Attribute and Size Register %d'  % i) for i in range(4) ),

                # Floating Point Unit
                ('CPACR' , word, 0xe000ed88, 'Coprocessor Access Control Register'),
                ('FPCCR' , word, 0xe000ef34, 'Floating-point Context Control Register'),
                ('FPCAR' , word, 0xe000ef38, 'Floating-point Context Address Register'),
                # TODO: what about FPSCR?
                ('FPDSCR', word, 0xe000ef3c, 'Floating-point Default Status Control Register'),

                # Cache Maintenance Operations
                ('ICIALLU' , word, 0xe000ef50, 'Instruction cache invalidate all to the Point of Unification'),
                ('ICIMVAU' , word, 0xe000ef58, 'Instruction cache invalidate by address to the Point of Unification'),
                ('DCIMVAC' , word, 0xe000ef5c, 'Data cache invalidate by address to the Point of Coherency'),
                ('DCISW'   , word, 0xe000ef60, 'Data cache invalidate by set/way'),
                ('DCCMVAU' , word, 0xe000ef64, 'Data cache clean by address to the Point of Unification'),
                ('DCCMVAC' , word, 0xe000ef68, 'Data cache clean by address to the Point of Coherency'),
                ('DCCSW'   , word, 0xe000ef6c, 'Data cache clean by set/way'),
                ('DCCIMVAC', word, 0xe000ef70, 'Data cache clean and invalidate by address to the Point of Unification'),
                ('DCCISW'  , word, 0xe000ef74, 'Data cache clean and invalidate by set/way'),
                ('BPIALL'  , word, 0xe000ef78, 'The BPIALL register is not implemented'),

                ('ITCMCR', word, 0xe000ef90, 'Instruction Tightly-Coupled Memory Control Register'),
                ('DTCMCR', word, 0xe000ef94, 'Data Tightly-Coupled Memory Control Register'),
                ('AHBPCR', word, 0xe000ef98, 'AHBP Control Register'),
                ('CACR'  , word, 0xe000ef9c, 'L1 Cache Control Register'),
                ('AHBSCR', word, 0xe000efa0, 'AHB Slave Control Register'),
                ('ABFSR' , word, 0xe000efa8, 'Auxiliary Bus Fault Status Register'),

                ])

        return [ vector_table, private_peripheral_bus ]

if __name__ == '__main__':
    from pprint import pprint
    cm = CortexM(7, 0x08000000, 96)
    pprint(cm.get_registers())
