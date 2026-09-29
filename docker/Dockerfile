# Everything runs here; nothing is installed on the host. CPU only.
FROM python:3.12-slim
RUN pip install --no-cache-dir numpy==2.1.3 opencv-python-headless==4.10.0.84 ruff==0.8.4
ENV HOME=/tmp
WORKDIR /w
