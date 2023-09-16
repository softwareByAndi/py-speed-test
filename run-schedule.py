import schedule
import time
import os

def job():
    os.system('python speed-test.py')

schedule.every(20).minutes.do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(20*60)
