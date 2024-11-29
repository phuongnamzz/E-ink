## Cross compile C program on raspberry from Ubuntu 
Ref: [Raspberry Pi: How to cross-compile against third-party libraries](https://deardevices.com/2019/12/25/raspberry-pi-sysroot/)
[Using WiringPi library with Raspberry PI cross-compiler](https://visualgdb.com/tutorials/raspberry/wiringPi/)
1. First, install all library on raspberry
2. Run, and test with all library
3. Copy folders as /lib, /usr/lib, /usr/include, /usr/local/ (/usr/local will have include & lib)
`rsync -avzh pi@pi.local:/lib sysroot` ...
4. Create a new sysroot folder and paste all folders in step 3 to it 
5. Configure Makefile like this 
`SYSROOT = /home/pnam/raspi-sysroot`
`TARGET = epd`
`CC = arm-linux-gnueabihf-gcc`
`MSG = -g -O -ffunction-sections -fdata-sections -Wall` 
`CFLAGS = $(MSG) -D $(EPD)  --sysroot=$(SYSROOT)`
`CFLAGS += -I$(SYSROOT)/usr/include` 
`LDFLAGS = -L$(SYSROOT)/usr/lib -lwiringPi -lcrypt`
`RPI_epd:${OBJ_O}`
	`echo $(@)`
	`$(CC) $(CFLAGS) -D RPI $(OBJ_O) $(RPI_DEV_C) -o $(TARGET) $(LIB_RPI) $(DEBUG) $(LDFLAGS)`	
### Note : Glibc version same between host and raspberry 

## Convert font to Vietnamese need Unicode UTF-8 C language
Waveshare e-paper lib for raspberry, Arduino, ESP32, STM32 https://github.com/waveshareteam/e-Paper support C and Python.
