# Fortress Threat Detection and Response Engine

Fortress Threat Detection and Response Engine queries event data Fortress Event Consumer saves to database and decides if a event is threat. The engine runs anomaly detection algorithm both on event and transaction data to see if an abnormal event pattern occurs. It also runs security audit for for events that change the contract, interact with unaudited contracts or create any risk according to predefined settings. After detecting a threat the engine decides on the response according to predefined set of responses.

## Installation

pip3 install -r requirements.txt (

## How To Use

python3 run.py



