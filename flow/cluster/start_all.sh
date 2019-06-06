#!/bin/bash
parallel-ssh -h master.txt -P -I < start_master.sh
parallel-ssh -h workers.txt -P -I < start_worker.sh
