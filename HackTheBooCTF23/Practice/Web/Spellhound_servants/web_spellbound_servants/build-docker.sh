#!/bin/bash
docker rm -f web_spellbound_servants
docker build --tag=web_spellbound_servants .
docker run -p 1337:1337 --rm --name=web_spellbound_servants web_spellbound_servants