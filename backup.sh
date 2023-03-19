#!/bin/bash

if [ -z "$RESTIC_REPOSITORY" ]; then
  echo "Error: RESTIC_REPOSITORY environment variable is not set"
  exit 1
fi

if [ -z "$RESTIC_PASSWORD" ]; then
  echo "Error: RESTIC_PASSWORD environment variable is not set"
  exit 1
fi

BACKUP_SOURCE=~/content-collector/data

restic backup $BACKUP_SOURCE