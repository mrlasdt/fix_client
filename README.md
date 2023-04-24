# Overview
This application is a FIX client that communicates with a FIX server and implements a simple trading strategy.


## Project structure
```
├── config
│   ├── dtl.cfg
│   ├── FIX42_DTL.xml
│   └── settings.yml
├── main.py
├── requirements.txt
└── src
    ├── command
    │   ├── start_command.py
    │   └── stop_command.py
    ├── common
    │   ├── clock.py
    │   ├── dto.py
    │   ├── logger.py
    │   ├── order_tracker.py
    │   └── timer.py
    ├── fix_client
    │   ├── base_fix_client.py
    │   └── dtl_fix_client.py
    └── strategy
        ├── base_strategy.py
        └── dtl_strategy.py
```

The config directory contains configuration files such as dtl.cfg, FIX42_DTL.xml, and settings.yml. 
The main.py file is the entry point of the application. The src directory contains the source code of the application, which is further divided into subdirectories such as command, common, fix_client, and strategy.

- command: Contains command objects to execute start and stop commands.
- common: Contains common utility classes such as clock, dto, logger, order_tracker, and timer.
- fix_client: Contains classes related to the FIX client implementation.
- strategy: Contains classes related to the trading strategy implementation.

## Installation
- Python version: 3.9
- Install the required packages using the requirements.txt file:
```
pip install -r requirements.txt

```
## Configuration
Configure the application using the configuration files in the config directory. dtl.cfg and FIX42_DTL.xml contain the FIX protocol configuration details. settings.yml contains the application-specific settings such as tick size and order quantity.
## Usage
Start the application by running the `main.py` file:
```
python main.py
```
## Implementation details
- At the initialization stage, the application instantiates all the required objects such as the FIX client, the trading strategy, the order tracker, and the clocks.

- Every tick size (configured in the settings.yml file) of clock: 
    + The trading strategy randomly sends 1 new order and 1 new cancel order request. 
    + The FIX client, besides maintaining a socket to communicate with the server, checks for all expired orders and cancels them. 
    + The Order Tracker is in charge of handle orders status base on the type of message receive from the server (35=3|35=8|35=9).

- After 1000 orders are sent and processed, the application reports total volume, PNL, and VWAP as required.

- The results is as follows:
```
[INFO]: Total volume is 13180579.39 USD
[INFO]: PNL is 60354.39 USD
[INFO]: VWAP of MSFT is 240.18
[INFO]: VWAP of AAPL is 151.52
[INFO]: VWAP of BAC is 32.46
[INFO]: Total run time took : 105.291122 seconds
```

## Limitations
- The application was unable to send Order Cancel Request (35=F) because the error:
```
8=FIX.4.2|9=119|35=9|34=794|49=DTL|52=20230424-09:17:12.559|56=OPS_CANDIDATE_8_1142|11=00453|37=NONE|39=8|41=00344|58=Unknown order id|10=177|
```
The sent cancel requests did include the order id (tag 44) but was still rejected.


