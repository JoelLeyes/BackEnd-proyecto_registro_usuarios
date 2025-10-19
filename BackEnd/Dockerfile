# Dockerfile para users-api-service (Django)
FROM python:3.11-slim
WORKDIR /app
COPY BackEnd/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY BackEnd/ /app/
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
