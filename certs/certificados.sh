#!/bin/bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /inoichi/certs/opensearch.key -out /inoichi/certs/opensearch.crt
