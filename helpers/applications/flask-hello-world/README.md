# Flask Hello World

A simple Flask app running on Docker (or not). You can use the Docker file to create the container or just use the content of the `scr` folder for your own application

## Running the example

```shell
docker build -t flask-hello-world:latest .
docker run -d -p 5000:5000 flask-hello-world
```
