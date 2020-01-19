#!/bin/bash
parallel-ssh -h master.txt -P -I < stop_worker.sh
parallel-ssh -h workers.txt -P -I < stop_worker.sh
