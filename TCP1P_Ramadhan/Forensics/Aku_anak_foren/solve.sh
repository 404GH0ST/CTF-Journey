#!/bin/bash

tshark -Y http.request.method==POST -Tfields -e http.file_data -r capture.pcap | xxd -r -p
