# Verwenden eines Basis Images
FROM python:3.10

# Definition des Arbeitsverzeichnisses
WORKDIR /app

# Kopieren des Codes
COPY . /app

# Installieren der Abhängigkeitn
RUN pip install -r requirements.txt

# Verfügbarkeit des Ports
EXPOSE 8000

# Start Applikation
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]