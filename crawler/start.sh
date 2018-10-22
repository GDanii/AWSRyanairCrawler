#!/bin/bash
service awslogs start
echo Started
service awslogs status
python /app/crawl.py $FROM $TO