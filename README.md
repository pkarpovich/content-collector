# Content collector

## Description
This is a simple application that collects playing content from local Apple TV and stores it in a database

## Environment Variables
* `ATV_NAME` - Name of the Apple TV
* `ATV_ID` - ID of the Apple TV
* `ATV_AIR_PLAY_CREDENTIALS` - AirPlay credentials of the Apple TV
* `ATV_COMPANION_CREDENTIALS` - Companion credentials of the Apple TV
* `ATV_RAOP_CREDENTIALS` - RAOP credentials of the Apple TV
* `DATABASE_PATH` - Path to the database file
* `SLEEP_TIMEOUT` - Time to sleep between each collect in seconds

## Commands
* `make backup` - Make a backup of the database
* `make redeploy` - Redeploy the application

## Backups
This application data could be backup by restic. To do so, you need to setup repository:
```bash
restic init -r /path/to/repo
```
Set environment variables for repository:
```bash
export RESTIC_PASSWORD=your_password
export RESTIC_REPOSITORY=/path/to/repo
```
Make a backup file executable:
```bash
chmod +x backup.sh
```
Schedule a backup with cron if needed:
```bash
crontab -e

0 0 * * * /path/to/backup.sh
```