FROM python:3.9

WORKDIR /usr/project/
COPY . .
#VOLUME ["/usr/project/log"]

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -U --no-cache-dir -r requirements.txt


CMD ["/usr/project/entrypoint.sh"]