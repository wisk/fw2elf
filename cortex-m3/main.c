typedef unsigned int stack_t;
typedef void (*handler_t)(void);
typedef unsigned int u32_t;

struct {
	stack_t InitialSP;
	handler_t Reset;
	handler_t NMI;
	handler_t HardFault;
	handler_t MemManageFault;
	handler_t BusFault;
	handler_t UsageFault;
	handler_t Reserved0[4];
	handler_t SVCall;
	handler_t DebugMonitor;
	handler_t Reserved1;
	handler_t PendSV;
	handler_t SysTick;
	handler_t IRQ[0];
} IV __attribute__((section(".iv")));


struct {
	u32_t MasterCtrl;
	u32_t IntCtrlType;
	u32_t zReserved008_00c[2];
	/* Reserved space */
	struct {
		u32_t Ctrl;
		u32_t Reload;
		u32_t Value;
		u32_t Calibration;
	} SysTick;
	u32_t zReserved020_0fc[(0x100-0x20)/4];
	/* Reserved space */
	/* Offset 0x0100 */
	struct {
		u32_t Enable[32];
		u32_t Disable[32];
		u32_t Set[32];
		u32_t Clear[32];
		u32_t Active[64];
		u32_t Priority[64];
	} NVIC;
	u32_t zReserved0x500_0xcfc[(0xd00-0x500)/4];
	/* Reserved space */
	/* Offset 0x0d00 */
	u32_t CPUID;
	u32_t IRQcontrolState;
	u32_t ExceptionTableOffset;
	u32_t AIRC;
	u32_t SysCtrl;
	u32_t ConfigCtrl;
	u32_t SystemPriority[3];
	u32_t SystemHandlerCtrlAndState;
	u32_t ConfigurableFaultStatus;
	u32_t HardFaultStatus;
	u32_t DebugFaultStatus;
	u32_t MemManageAddress;
	u32_t BusFaultAddress;
	u32_t AuxFaultStatus;
	u32_t zReserved0xd40_0xd90[(0xd90-0xd40)/4];
	/* Reserved space */
	/* Offset 0x0d90 */
	struct {
		u32_t Type;
		u32_t Ctrl;
		u32_t RegionNumber;
		u32_t RegionBaseAddr;
		u32_t RegionAttrSize;
	} MPU;
} SCS __attribute__((section(".scs")));
