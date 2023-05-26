#define F_CPU 16000000UL

#include <avr/io.h>

#include <avr/interrupt.h>

#include <util/delay.h>

volatile unsigned char rx_data;

volatile int do_tx = 0;

ISR(USART0_RX_vect){

	rx_data = UDR0;

	do_tx = 1;

}

void main(void){

	.	unsigned char ucaFndHex[] = { 0x73, 0x1E, 0x6D, 0x6E, 0x76, 0x39, 0xB7, 0xBE };//P,J,S,Y,H,C,M,W

	

	DDRA = 0xFF;

	PORTE = 0xFF;

	

	DDRC = 0xFF;

	DDRG = 0x0F;

	

	UBRR0H = 103 >> 8;

	UBRR0L = 103;

	UCSR0A = 0x00;

	UCSR0B = 0x98;

	UCSR0C = 0x06;

	rx_data = UDR0;

	SREG = 0x80;

	while(1){

		if (do_tx)

		{

			do_tx = 0;

			while(!(UCSR0A & 0x20));

			UDR0 = rx_data;

			

			PORTA = 0xFF;

			_delay_ms(10);

			PORTA = 0x0;

		}

		if (rx_data == '1')

		{

			PORTC = ucaFndHex[0];

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = ucaFndHex[1];

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = ucaFndHex[2];

			PORTG = 0x02;

			_delay_ms(5);

		}

		else if (rx_data == '0')

		{

			PORTC = ucaFndHex[3];

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = ucaFndHex[1];

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = ucaFndHex[4];

			PORTG = 0x02;

			_delay_ms(5);

		}

		else if (rx_data == '4')

		{

			PORTC = ucaFndHex[2];

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = ucaFndHex[6];

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = ucaFndHex[4];

			PORTG = 0x02;

			_delay_ms(5);

		}

		else if (rx_data == '3')

		{

			PORTC = ucaFndHex[5];

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = ucaFndHex[7];

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = ucaFndHex[2];

			PORTG = 0x02;

			_delay_ms(5);

		}

		else if (rx_data == '2')

		{

			PORTC = ucaFndHex[1];

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = ucaFndHex[2];

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = ucaFndHex[4];

			PORTG = 0x02;

			_delay_ms(5);

		}

		else { PORTC = 0;

			PORTG = 0x08;

			_delay_ms(5);

			PORTC = 0;

			PORTG = 0x04;

			_delay_ms(5);

			PORTC = 0;

			PORTG = 0x02;

			_delay_ms(5);}

	}

	

}
