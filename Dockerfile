FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3.11 python3-pip \
    ffmpeg zstd p7zip-full brotli ghostscript \
    webp jpegoptim optipng pngquant \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
