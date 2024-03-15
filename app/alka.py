from sqlalchemy import create_engine

# Создайте Engine
engine = create_engine('postgresql://neohack:CectGfJj0TEhKlvUmN_0hQ@neo-hack-vacantion-14064.8nj.gcp-europe-west1.cockroachlabs.cloud:26257/neohack-vacation-website?sslmode=verify-full', echo=True)
