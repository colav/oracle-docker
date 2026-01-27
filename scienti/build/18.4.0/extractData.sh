#!/bin/bash

echo "======================================"
echo "Executing data extraction with Kaypacha"
echo "======================================"

BASENAME=$(basename "$CVLAC_USER")

PREFIX=$(echo "$BASENAME" | cut -d '_' -f 1)

MONGO_DBNAME="scienti_${PREFIX}_${DUMP_DATE}"

CMD="kaypacha_scienti \
    --mongo_dbname ${MONGO_DBNAME} \
    --mongo_dburi ${MONGO_DBURI} \
    --model product \
    --max_threads 2 \
    --cvlac_user ${CVLAC_USER} \
    --gruplac_user ${GRUPLAC_USER} \
    --institulac_user ${INSTITULAC_USER} \
    --checkpoint"

echo "Executing Kaypacha..."
echo "$CMD"
$CMD
EXIT_CODE=$?

echo
if [ $EXIT_CODE -eq 0 ]; then
    echo "Kaypacha finished successfully"
else
    echo "Error running Kaypacha, code: $EXIT_CODE"
fi
