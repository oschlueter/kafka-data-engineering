# Kafka Data Engineering Challenge

This prototype demonstrates the use of [Apache Kafka](https://kafka.apache.org/) to process Wikipedia edits and calculate rates of page edits.

## Requirements

This prototype depends on 

* Python 3.9+
* pip
* Docker
* docker-compose
* GNU Make
* [kcat](https://github.com/edenhill/kcat) (formerly known as kafkacat; optional)

## Setup

Optionally, create a Python virtual environment for this project:

    python3 -m venv venv
    source venv/bin/activate
    pip install -U pip

Install the Python requirements:

    pip install -r requirements.txt

Ensure `host.docker.internal` resolves to `localhost` on the host machine.
On MacOS you can achieve this as follows:

    echo  '127.0.0.1   host.docker.internal' | sudo tee -a /private/etc/hosts

## Usage

Start Apache Kafka and create required topics:

    make create-topics

Run the producer and consumer:

    python producer.py & 
    python consumer.py

The consumer will start printing the edits per minute to stdout after 60 seconds.
Cancel the consumer with `Ctrl-C` when all edit events have been processed, i.e., after 500 seconds on average.

Clean up Docker resources:

    make down

## Development

Use kcat to inspect content of Kafka topics, for example

    make read-de

Run pytests with

    make test

## License
[MIT](https://choosealicense.com/licenses/mit/)