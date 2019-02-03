#pragma once

typedef unsigned int uint32_t;

typedef volatile struct {
	uint32_t MasterCtrl;
	uint32_t IntCtrlType;
	uint32_t zReserved008_00c[2];
	/* Reserved space */
	struct {
		uint32_t Ctrl;
		uint32_t Reload;
		uint32_t Value;
		uint32_t Calibration;
	} SysTick;
	uint32_t zReserved020_0fc[(0x100-0x20)/4];
	/* Reserved space */
	/* Offset 0x0100 */
	struct {
		uint32_t Enable[32];
		uint32_t Disable[32];
		uint32_t Set[32];
		uint32_t Clear[32];
		uint32_t Active[64];
		uint32_t Priority[64];
	} NVIC;
	uint32_t zReserved0x500_0xcfc[(0xd00-0x500)/4];
	/* Reserved space */
	/* Offset 0x0d00 */
	uint32_t CPUID;
	uint32_t IRQcontrolState;
	uint32_t ExceptionTableOffset;
	uint32_t AIRC;
	uint32_t SysCtrl;
	uint32_t ConfigCtrl;
	uint32_t SystemPriority[3];
	uint32_t SystemHandlerCtrlAndState;
	uint32_t ConfigurableFaultStatus;
	uint32_t HardFaultStatus;
	uint32_t DebugFaultStatus;
	uint32_t MemManageAddress;
	uint32_t BusFaultAddress;
	uint32_t AuxFaultStatus;
	uint32_t zReserved0xd40_0xd90[(0xd90-0xd40)/4];
	/* Reserved space */
	/* Offset 0x0d90 */
	struct {
		uint32_t Type;
		uint32_t Ctrl;
		uint32_t RegionNumber;
		uint32_t RegionBaseAddr;
		uint32_t RegionAttrSize;
	} MPU;
} SCS_t;
