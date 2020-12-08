# Fortress Threat Detection and Response Engine

Fortress Threat Detection and Response Engine queries event data [Fortress Event Consumer](https://github.com/fortressfoundation/fortress-event-consumer) saves to mongoDB database and makes analysis on whether the event or set of events is a threat to the DeFi app. The engine runs anomaly detection algorithm both on event and transaction data to see if an abnormal event pattern occurs. It is also responsible from running [Fortress Live Security Audit](https://github.com/fortressfoundation/fortress-security-audit-engine) for events that change the contract, interact with unaudited contracts or create any risk according to community defined threat patterns. If the engine detects threat after anomaly detection or security audit, it terminates contract execution. In the coming versions we will be working on giving responses according to community defined industry standards.

## Installation

pip3 install -r requirements.txt

## How To Use

python3 run.py

NOTE: This is Pre-Alpha Release. Development for stable alpha release is being done and this may work unstable at the moment.




