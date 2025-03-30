#!/bin/bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout opensearch.key -out opensearch.crt
