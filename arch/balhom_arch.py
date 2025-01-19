from urllib.request import urlretrieve

from diagrams import Cluster, Diagram
from diagrams.onprem.database import Postgresql, Cassandra, Mongodb
from diagrams.onprem.network import Traefik
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
from diagrams.firebase.develop import Authentication
from diagrams.programming.framework import Spring, FastAPI

# Supabase
supabase_url = "https://avatars.githubusercontent.com/u/54469796?s=200&v=4"
supabase_icon = "supabase.png"
urlretrieve(supabase_url, supabase_icon)

# Kafka
kafka_url = "https://svn.apache.org/repos/asf/kafka/site/logos/originals/png/ICON%20-%20Black%20on%20Transparent.png"
kafka_icon = "kafka.png"
urlretrieve(kafka_url, kafka_icon)

# MinIO
minio_url = "https://min.io/resources/img/logo/MINIO_Bird.png"
minio_icon = "minio.png"
urlretrieve(minio_url, minio_icon)

# Gin Gonic
gin_gonic_url = "https://raw.githubusercontent.com/gin-gonic/logo/master/color.png"
gin_gonic_icon = "gin_gonic.png"
urlretrieve(gin_gonic_url, gin_gonic_icon)

with Diagram("Balhom Arch", show=True):

    # Currency Profiles Cluster
    with Cluster("Currency Profiles Service"):
        with Cluster("Currency Profiles API"):
            currency_profiles_api = Server()
            Spring()
        currency_profiles_db = Mongodb("DB")
        currency_profiles_object_storage = Custom("Object Storage", minio_icon)

        currency_profiles_api >> currency_profiles_db
        currency_profiles_api >> currency_profiles_object_storage

    # Transactions Cluster
    with Cluster("Transactions Service"):
        with Cluster("Transactions API"):
            transactions_api = Server()
            Spring()
        transactions_db = Postgresql("DB")
        transactions_object_storage = Custom("Object Storage", minio_icon)

        transactions_api >> transactions_db
        transactions_api >> transactions_object_storage

    # Savings Cluster
    with Cluster("Savings Service"):
        with Cluster("Savings API"):
            savings_api = Server()
            Custom("", gin_gonic_icon)
        savings_db = Cassandra("DB")

        savings_api >> savings_db

    with Cluster():
        with Cluster("Users API"):
            users_api = Server()
            FastAPI()
        users_db = Mongodb("DB")
        supabase_auth = Custom("Supabase Auth", supabase_icon)
        
        users_api >> users_db
        users_api >> supabase_auth

    api_gateway = Traefik("Api Gateway")

    kafka = Custom("Kafka", kafka_icon)


    api_gateway >> users_api
    api_gateway >> currency_profiles_api
    api_gateway >> transactions_api
    api_gateway >> savings_api

    transactions_api >> kafka
    kafka >> currency_profiles_api
    kafka >> savings_api

    currency_profiles_api >> users_api
    transactions_api >> currency_profiles_api
    savings_api >> currency_profiles_api
