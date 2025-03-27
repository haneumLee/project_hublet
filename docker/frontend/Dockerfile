FROM python:3.11-slim

WORKDIR /app
COPY frontend/monitoring /app

RUN pip install --no-cache-dir streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]