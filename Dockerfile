FROM python:3
RUN pip install mkdocs mkdocs-material

ADD . .
RUN pip install -r requirements.txt .

# Start development server by default
ENTRYPOINT ["mkdocs"]