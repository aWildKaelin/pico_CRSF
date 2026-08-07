# pico_CRSF


This project provides a parser for the TBS Crossfire (CRSF) protocol for the RP2040/Raspberry Pi Pico family of microcontrollers. CRSF is the protocol used by TBS Crossfire and ExpressLRS (ELRS) receivers to communicate with a host controller. Thus, this libarry allows for the use of standard drone RC hardware to control other robots and machines based on the RP2040 microcontroller.

Compatibility with the RP2350 (Raspberry Pi Pico 2) has not been tested.

## Features

Currently, the library is capable of parsing incoming packets, including RC Channels and Link Statistics.

The library cannot transmit packets back or parse other telemetry.

# WARNING

The RP2040 is a **3.3 V** microcontroller. Applying **5 V UART logic levels** to its GPIO pins **can permanently damage the microcontroller**.

Before connecting a receiver, verify that its UART TX output uses 3.3 V logic. If it outputs 5 V logic, use an appropriate logic level converter.

## Usage

Create a `crsf_parser` struct.
```c
crsf_parser parser;
```

Apply the correct UART configuration. For most ELRS receiver, the appropriate baud rate is 420000.
```c
// for ELRS, use this baud rate
uart_init(UART_ID, 420000);

gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
```

Initialize the parser:
```c
CRSFParser_init(&parser, UART_ID);
```

Call `CRSFParser_update()` periodically from your main loop to continue receiving and decoding packets.
```c
// main loop
while(true){
    CRSFParser_update(&parser);

    //your code here
}
```

The parser structure always contains the most recently decoded values for each supported packet type.
```c
// channel data
parser.RCChannels.channel_NUM //where NUM is the channel number ranging 1 -> 16
parser.statistics.VAL         // where VAL is a value contained within the packet. See  crsf_packets.h  for details
```

By default, most transmitters use the **AETR1234** channel mapping:
```
Channel 1 -> Roll (Aileron)
Channel 2 -> Pitch (Elevator)
Channel 3 -> Throttle
Channel 4 -> Yaw (Rudder)
Channel 5 -> AUX1
Channel 6 -> AUX2
...
```
Channel values are decoded as standard CRSF 11-bit channel values (typically
approximately 172–1811, with center at 992).

If you need to regenerate the CRC8 table or to change the generator polynomial, modify the `POLY` constant at the top of `crc8_generator.py` and run it in your terminal using `python crc8_generator.py`. The result can be directly pasted into the `crsf_parser.c` file.

## Setup

This project is intended for use with the `Raspberry Pi Pico SDK`, built and tested using Visual Studio Code.

To use in your project, simply copy the pico_crsf folder and the `LICENSE.md` file into your project and append to your `CMakeLists.txt`:
```cmake
add_subdirectory(pico_crsf)
target_link_libraries(your_project pico_crsf)
```

Then, include `"pico_crsf/crsf_parser.h"`.


## Contributions

Contributions and forks are welcome.

Please keep in mind that CRSF packets use big-endian byte ordering, while the RP2040 is a little-endian architecture.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

This library implements the CRSF V3 protocol as specified in the [CRSF V3 Protocol Specification](https://github.com/tbs-fpv/tbs-crsf-spec/tree/main).

The specification is © 2020 [TBS Avionics Co LTD](https://team-blacksheep.com) and is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1).

This project is not affiliated with or endorsed by TBS Avionics Co LTD or the ExpressLRS project.
