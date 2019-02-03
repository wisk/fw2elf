#pragma once

typedef unsigned int stack_t;
typedef void (*handler_t)(void);

typedef struct {
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
} IV_t;
