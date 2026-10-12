#!/bin/bash
lab06_port81_type() {
    awk '$2 == "tcp" { for (i=3; i<=NF; i++) { gsub(/,/, "", $i); if ($i == "81") print $1 } }'
}
