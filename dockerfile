FROM python:3.9
LABEL maintainer="apicebas"
WORKDIR /work
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./api.py"]