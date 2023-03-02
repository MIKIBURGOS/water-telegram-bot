import csv
import datetime
import schedule
import time
import Telegram_bot as telegram_bot


def reminders():
    pass
    # recordatorios a lo largo del día para beber
    # recordatorios cuando se pasa mucho tiempo sin hacer una actividad

def main():
    schedule.every().day.at("00:00").do(telegram_bot.new_day)

    while True:
        schedule.run_pending()
        time.sleep(1)

main()