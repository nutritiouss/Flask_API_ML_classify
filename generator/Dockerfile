FROM python:3.9
WORKDIR /var/app
COPY ./ ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN  pip install -r  /var/app/requirements.txt
CMD ["python3", "generator.py", "runserver"]


