FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./parking_handler.py ./invokes.py ./
CMD [ "python", "./parking_handler.py" ]