#include "tracer.h"

#include "stm32.h"

enum tracer_event {
	TRACER_EVENT_ENTER = 0,
	TRACER_EVENT_EXIT = 1,
};

void tracer_enter(uint8_t id) {
	usart_write(USART1, TRACER_EVENT_ENTER);
	usart_write(USART1, id);
}

void tracer_exit(uint8_t id) {
	usart_write(USART1, TRACER_EVENT_EXIT);
	usart_write(USART1, id);
}
