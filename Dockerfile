# 1. Base Image: Python ka stable version
FROM python:3.10-slim

# 2. Working Directory set karo container ke andar
WORKDIR /app

# 3. System dependencies install karo (SQLite aur basic tools ke liye)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Requirements copy aur install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Pura project code container mein copy karo
COPY . .

# 6. Ports Open karo (8000 Backend ke liye, 8501 Frontend ke liye)
EXPOSE 8000
EXPOSE 8501

# 7. Start Script: Dono servers (FastAPI aur Streamlit) ko ek saath chalane ke liye
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0"]