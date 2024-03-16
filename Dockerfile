FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TOKEN="7124366582:AAEv02uyhYre5uByMZiZDhlGHqOKG3Yj7o0" \
    MONGOURL="mongodb://localhost:27017/" \
    SERVER_ENDP="http://127.0.0.1:8000/api/v1/tour/" \
    ENGINE_URL="cockroachdb://neohack:CectGfJj0TEhKlvUmN_0hQ@neo-hack-vacantion-14064.8nj.gcp-europe-west1.cockroachlabs.cloud:26257/neohack-vacation-website"

CMD ["python", "app/main.py"]