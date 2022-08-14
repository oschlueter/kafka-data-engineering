BROKER=localhost:9092

read-wiki-edits: TOPIC=wiki-edits
read-global: TOPIC=edits-per-minute-global
read-de: TOPIC=edits-per-minute-de

list-topics:
	kcat -b $(BROKER) -L

read-wiki-edits read-global read-de:
	kcat -b $(BROKER) -t $(TOPIC)

send-wiki-edit:
	echo 'hello' | kcat -b $(BROKER) -t wiki-edits -z snappy

create-topics: up
	for topic in wiki-edits edits-per-minute-global edits-per-minute-de; do \
		docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic $$topic --bootstrap-server localhost:9092 ; \
	done

down:
	docker-compose down
	docker volume prune -f

up:
	docker-compose up -d

logs:
	docker-compose logs -f

test:
	pytest
