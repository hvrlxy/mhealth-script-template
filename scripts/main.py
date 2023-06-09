from unzip_all import UnZip
from auto_scp import AutoSCP
import warnings
import os
import logging
import datetime
import traceback

warnings.filterwarnings("ignore")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/..'
nums_day = 4
subjects = ['user01', 'user02']

# get today's date as format YYYY-MM-DD
today = datetime.datetime.today().strftime('%Y-%m-%d') 

logs_path = os.path.dirname(os.path.abspath(__file__)) + '/..' + '/logs/' + today

# create a logs folder of today's date if it doesn't exist
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

# set up a logger for the main class
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# set the log file
log_file = logs_path + '/main.log'
# set the log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# set the log file handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

# put the file handler in the logger
logger.addHandler(file_handler)

# get yesterday's date as format YYYY-MM-DD
yesterday = datetime.datetime.today()
# get a list of the last 10 days from yesterday with format YYYY-MM-DD
last_10_days = [yesterday - datetime.timedelta(days=x) for x in range(0, nums_day)]
last_10_days = [day.strftime('%Y-%m-%d') for day in last_10_days]
# initialize the auto scp class
auto_scp = AutoSCP()

# initialize the unzip class
unzip = UnZip()

# get the data from the server for the last num_days
for day in last_10_days:
    for subject in subjects:
        logger.info('Getting data for subject: ' + subject + ' for day: ' + day)
        # get logs-watch 
        try:
            auto_scp.get_logs_watch(subject, day)
        except Exception as e:
            logger.error('Error getting logs-watcher logs for day: ' + day)
            logger.error(traceback.format_exc())
            print('Error getting logs-watcher logs for day: ' + day)
        logger.info('Finished getting data for subject: ' + subject + ' for day: ' + day)
        try:
            auto_scp.get_data(subject, day)
        except Exception as e:
            logger.error('Error getting data for day: ' + day)
            logger.error(traceback.format_exc())
            print('Error getting logs-watcher logs for day: ' + day)
        try:
            auto_scp.get_logs(subject, day)
        except Exception as e:
            logger.error('Error getting logs for day: ' + day)
            logger.error(traceback.format_exc())
            print('Error getting logs-watcher logs for day: ' + day)
        # get data-watcher logs
        try:
            auto_scp.get_data_watch(subject, day)
        except Exception as e:
            logger.error('Error getting data-watcher logs for day: ' + day)
            logger.error(traceback.format_exc())
        print('Finished getting data for subject: ' + subject + ' for day: ' + day)
    # time.sleep(5)

# unzip all the files
unzip.unzip_all(days=nums_day, subject_list=subjects)
