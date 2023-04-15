import schedule
import time
from modules.healthchecker import Healthchecker
from pyhocon import ConfigFactory


conf = ConfigFactory.parse_file('hocon.conf')

bot_token = conf.get('notification.telegram.token')
chat_id = conf.get('notification.telegram.chat_id')

influx_token = conf.get('influxdb.influx_token')
influx_bucket = conf.get('influxdb.bucket')
influx_org = conf.get('influxdb.org')
influx_server = conf.get('influxdb.server')

path_to_server_list = conf.get('servers.path_to_list')
timeout = int(conf.get('monitoring.timeout'))
notify_time = conf.get('monitoring.notify_time')

log_path = conf.get('notification.logging.log_path')
log_mode = conf.get('notification.logging.log_mode')

hc = Healthchecker(path_to_server_list,
                   bot_token,
                   chat_id,
                   influx_token,
                   influx_bucket,
                   influx_org,
                   influx_server)

schedule.every(timeout).seconds.do(hc.check_servers_status)
schedule.every().day.at(notify_time).do(hc.notify_server_status)

while True:
    schedule.run_pending()
    time.sleep(1)

