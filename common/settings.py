# PostgreSQL DB configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "admin"
DB_NAME = "park_db"

# Kafka configuration
KAFKA_SERVERS = ["localhost:9092"]  # Servers are list of format ['host:post', 'host:port', ...]

# Application configuration
SLICER_CHECK_INTERVAL = 4
CLASSIFY_PERIOD_SECONDS = 20
