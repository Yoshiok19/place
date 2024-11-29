#!/bin/bash
docker build -t yoshiokd19/placesocketserver:latest .
docker run -p 8081:8081 -d yoshiokd19/placesocketserver:latest

