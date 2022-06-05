import os


KAFKA_TOPIK = os.getenv("KAFKA_TOPIK", "views")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHMS = os.getenv("JWT_ALGORITHMS", "HS256").split(",")
