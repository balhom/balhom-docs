from urllib.request import urlretrieve

from diagrams import Cluster, Diagram
from diagrams.onprem.database import Postgresql, Cassandra, Mongodb
from diagrams.onprem.network import Traefik
from diagrams.custom import Custom
from diagrams.programming.framework import Spring, Quarkus

# Keycloak
keycloak_url = "https://upload.wikimedia.org/wikipedia/commons/2/29/Keycloak_Logo.png"
keycloak_icon = "keycloak.png"
urlretrieve(keycloak_url, keycloak_icon)

# Kafka
kafka_url = "https://svn.apache.org/repos/asf/kafka/site/logos/originals/png/ICON%20-%20Black%20on%20Transparent.png"
kafka_icon = "kafka.png"
urlretrieve(kafka_url, kafka_icon)

# MinIO
minio_url = "https://avatars.githubusercontent.com/u/695951?s=200&v=4"
minio_icon = "minio.png"
urlretrieve(minio_url, minio_icon)

# Gin Gonic
gin_gonic_url = "https://avatars.githubusercontent.com/u/7894478?s=200&v=4"
gin_gonic_icon = "gin_gonic.png"
urlretrieve(gin_gonic_url, gin_gonic_icon)

with Diagram("Balhom Arch", show=True):

    # Currency Profiles Cluster
    with Cluster("Currency Profiles Service"):
        currency_profiles_api = Quarkus("Currency Profiles API")
        currency_profiles_db = Mongodb("DB")
        currency_profiles_object_storage = Custom("Object Storage", minio_icon)

        currency_profiles_api >> currency_profiles_db
        currency_profiles_api >> currency_profiles_object_storage

    # Transactions Cluster
    with Cluster("Transactions Service"):
        transactions_api = Spring("Transactions API")
        transactions_db = Postgresql("DB")
        transactions_object_storage = Custom("Object Storage", minio_icon)

        transactions_api >> transactions_db
        transactions_api >> transactions_object_storage

    # Statistics Cluster
    with Cluster("Statistics Service"):
        statistics_api = Custom("Statistics API", gin_gonic_icon)
        statistics_db = Cassandra("DB")

        statistics_api >> statistics_db

    keycloak_auth = Custom("Keycloak Auth", keycloak_icon)

    api_gateway = Traefik("Api Gateway")

    kafka = Custom("Kafka", kafka_icon)

    api_gateway >> keycloak_auth
    api_gateway >> currency_profiles_api
    api_gateway >> transactions_api
    api_gateway >> statistics_api

    transactions_api >> kafka
    kafka >> currency_profiles_api
    kafka >> statistics_api

    currency_profiles_api >> keycloak_auth
    transactions_api >> currency_profiles_api
    statistics_api >> currency_profiles_api
