# should start from `Ubuntu 24.04 LTS` or `python:3.12-slim` image, 
FROM python:3.12-slim
# # install git
RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*
# # clone the repo
RUN git clone --depth=1 https://github.com/nav128/aws_architetcture_recommader_server.git
# # set working directory
WORKDIR /aws_architetcture_recommader_server
RUN pip install setuptools
# pip install it
RUN pip install .
WORKDIR /aws_architetcture_recommader_server/src
# expose port 8000
EXPOSE 8080

# uv run the api server and on port 8000 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]