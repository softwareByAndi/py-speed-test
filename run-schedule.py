import schedule
import time
import os

MINUTES = 20

def job():
    os.system('python speed-test.py')

schedule.every(MINUTES).minutes.do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(MINUTES*60)
