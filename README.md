# Fortress Threat Detection and Response Engine

There are 2 use cases for threat detection

1. Engine queries event data [Fortress Event Consumer](https://github.com/fortressfoundation/fortress-event-consumer) saves to mongoDB database and makes analysis on whether the event or set of events is a threat to the DeFi app. The engine runs [HBOS](https://www.researchgate.net/publication/231614824_Histogram-based_Outlier_Score_HBOS_A_fast_Unsupervised_Anomaly_Detection_Algorithm) anomaly detection algorithm both on event and transaction data to see if an abnormal event pattern occurs.
2. Engine runs [Fortress Live Security Audit](https://github.com/fortressfoundation/fortress-security-audit-engine) for events that change the contract, interact with unaudited contracts or create any risk according to community defined threat patterns.

There is 1 use cases for threat response

1. If the engine detects threat after anomaly detection or security audit, it terminates contract execution. In the coming versions we will be working on giving responses according to community defined industry standards.

## Installation

pip3 install -r requirements.txt

## How To Use

1. Place fortress-security-audit-engine, fortress-event-listener, fortress-event-consumer and fortress-tdr-engine in the same directory
2. Update your DeFi app smart contract functions with the event listener function as stated in fortress-event-listener README so it will emit the events for threat detection before a contract change/transaction occurs. We choose not to do this automatically since it's your business logic. The idea is to check for a threat BEFORE an event occurs and stop it from happening if necessary.
3. Update fortress-event-consumer code according to events you've chosen to listen on fortress-event-listener as stated in README. In the next version(alpha) all consumer code will be generated automatically by running a script.
4. Run fortress-event-listener as stated in README. If you don't use Docker, make sure Kafka and MongoDB are running.
5. Run fortress-event-consumer as stated in README.
6. Make sure Prequisites for fortress-security-audit-engine are installed. Manually run the security audit on etherscan as imn the example above to check everything is working.
7. Run fortress-tdr-engine by "python3 run.py" command

Threat detection and Response engine will query the MongoDB database of events using the REST API that Fortress Event Consumer defines and will start looking for threat patterns on these events. If a pattern gets detected, it will automatically run security audit and stop/let the event contract execution according to events defined in fortress-event-listener

NOTE: This is Pre-Alpha Release. Development for stable alpha release is being done and this may work unstable at the moment.




