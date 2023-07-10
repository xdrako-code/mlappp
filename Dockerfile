FROM ubuntu:latest
WORKDIR /app
RUN apt update
RUN apt upgrade -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3-pip -y
RUN apt install libcairo2-dev -y
RUN apt install python3-dev -y
RUN apt install -y libpango1.0-dev
ENV PATH /usr/local/bin:$PATH
COPY requirements.txt requirements
COPY instance/ instance/
COPY . .
RUN pip3 install pycairo
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "mlapp.py"]
