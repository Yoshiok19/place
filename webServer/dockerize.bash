#!/bin/bash
docker build -t yoshiokd19/placewebserver:latest .
docker run -p 8080:8080 -d yoshiokd19/placewebserver:latest

