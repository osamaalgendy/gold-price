FROM python:3.13.3-alpine    #install latest python with alpine as base os 

WORKDIR /app    # set working directory

COPY . .   # copy all files from current directory to /app in container

RUN apk update --no-cache && apk upgrade --no-cache && apk add --no-cache git \
    && pip3 install --no-cache-dir -r requirements.txt # install dependencies from requirements.txt 

EXPOSE 8000   # expose port 8000 for fastapi
           
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]