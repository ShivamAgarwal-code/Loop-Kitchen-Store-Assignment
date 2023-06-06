import sqlite3
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Dict, List
import pytz
import pandas as pd


class StoreReport:
    def __init__(self, store_id):
        self.store_id = store_id
    
    def set_uptime_last_hour(self, active_minutes: int):
        self.uptime_last_hour = active_minutes

    def set_uptime_last_day(self, active_hours: int):
        self.uptime_last_day = active_hours

    def set_uptime_last_week(self, active_hours: int):
        self.uptime_last_week = active_hours

    def set_downtime_last_hour(self, inactive_minutes: int):
        self.downtime_last_hour = inactive_minutes
    
    def set_downtime_last_day(self, inactive_hours: int):
        self.downtime_last_day = inactive_hours

    def set_downtime_last_week(self, inactive_hours: int):
        self.downtime_last_week = inactive_hours
    
class TimingFunctions :
    def get_day_of_week(date: datetime)-> int:
        return date.weekday()

    def get_last_hour()->datetime:
        last_hour = datetime.today().astimezone(pytz.utc) - timedelta(hours = 1)
        return last_hour

    def get_last_week()->datetime:
        day = datetime.today().astimezone(pytz.utc)
        weekBefore = day - timedelta(days=7)
        return weekBefore

    def get_last_day()->datetime:
        today = datetime.today().astimezone(pytz.utc)
        last_day = today - timedelta(days = 1)
        return last_day

    def get_time_now()->datetime:
        return datetime.today().astimezone(pytz.utc)

    def construct_date(time_string: str, date: datetime)->datetime:        
        date_string = date.strftime("%d/%m/%Y")
        datetime_string = date_string +" "+ time_string
        
        return datetime.strptime(datetime_string, '%d/%m/%Y %H:%M:%S')

    def get_next_week_day(week_day: int)->int:
        return (week_day+1)%7

    def get_next_day(date: datetime) -> datetime:
        return date + timedelta(days=1)

class SQLiteOperations:

    def __init__(self, db_name:str):
        self.connection = None 
        self.cursor = None 
        self.connect(db_name)

    def connect(self, db_name:str)->None:
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def fetch_all_data_rows(self, table_name: str):
        if self.cursor == None:
            print("DB connection not made")
        else:
            rows = self.cursor.execute("SELECT * FROM "+table_name)
            return rows.fetchall()

    def fetch_all_stores(self):
        all_rows = self.fetch_all_data_rows("LK_STORE_TIMEZONES")
        all_stores = [row[0] for row in all_rows] # return only store IDs
        return all_stores

    def fetch_store_timings_on_day(self, store_id: int, day_of_week: int):
        row = self.cursor.execute("SELECT * FROM LK_MENU_HOURS WHERE STORE_ID=? AND DAY=?",(store_id, day_of_week))
        timings = row.fetchone()
        if timings == None or timings == []:
            return ['00:00:00','23:59:59']
        else:
            return timings[-2:]

    def fetch_store_activity(self, store_id: int, start_time: datetime, end_time: datetime):
        rows = self.cursor.execute("SELECT * FROM LK_STORE_STATUS WHERE STORE_ID=? AND TIMESTAMP_UTC BETWEEN ? AND ?",(store_id, start_time, end_time))
        return rows.fetchall()

    def fetch_store_timezone(self, store_id: int):
        rows = self.cursor.execute("SELECT timezone_str FROM LK_STORE_TIMEZONES WHERE STORE_ID=?",(store_id,))

        res = rows.fetchone()
        if(res == None or res == []) :
            return [store_id, 'America/Chicago']
        else:
            return res
        

## GLOBAL VARIABLES ##
sql_ops = SQLiteOperations("loopkitchen.db")
result: Dict[str, StoreReport] = {}
result_status: Dict[str, bool] = {}
result_lock = Lock()
sql_lock = Lock()
######################

#### HELPER FUNCTIONS #####
def find_store_timings_utc(store_id, timezone_str, curr_date):
    global sql_ops, sql_lock
    week_day = TimingFunctions.get_day_of_week(curr_date)
    sql_lock.acquire(blocking=True)
    [start_time, end_time] = sql_ops.fetch_store_timings_on_day(store_id, week_day)
    sql_lock.release()

    start_date_obj = TimingFunctions.construct_date(start_time, curr_date)
    end_date_obj = TimingFunctions.construct_date(end_time, curr_date)

    local = pytz.timezone(timezone_str)
    local_dt = local.localize(start_date_obj, is_dst=None)
    utc_starttime = local_dt.astimezone(pytz.utc)
    
    local_dt = local.localize(end_date_obj, is_dst=None)
    utc_endtime = local_dt.astimezone(pytz.utc)

    return [utc_starttime, utc_endtime]

def calculate_day_wise_activity(store_id: int, curr_date: datetime, timezone_str: str, begin_range: None or datetime, end_range: None or datetime, last_hour: bool = False) -> List[int] :
    global sql_ops
    pre_range , post_range = False, False
    duration = timedelta(0)
    [today_store_start , today_store_end] = find_store_timings_utc(store_id, timezone_str, curr_date)
    if begin_range!=None :
        if begin_range < today_store_start :
            yesterday = curr_date - timedelta(days=1)
            [_, yesterday_store_end] = find_store_timings_utc(store_id, timezone_str, yesterday)
            if yesterday_store_end >= begin_range :
                pre_range = True
                duration += (yesterday_store_end - begin_range)
        else:
            today_store_start = begin_range
    if end_range != None:
        if today_store_end < end_range:
            tomorrow = curr_date + timedelta(days=1)
            [tomorrow_store_start,_]=find_store_timings_utc(store_id, timezone_str,tomorrow)
            if tomorrow_store_start <= end_range:
                post_range = True
                duration += (end_range - tomorrow_store_start)
        else:
            today_store_end = end_range

    duration += (today_store_end - today_store_start)
    
    if(last_hour) : duration = duration.seconds / 60
    else : duration = duration.seconds / 3600

    sql_lock.acquire(blocking=True)
    activity = sql_ops.fetch_store_activity(store_id, today_store_start, today_store_end)
    if pre_range:
        temp_activity = sql_ops.fetch_store_activity(store_id, begin_range, yesterday_store_end)
        activity.extend(temp_activity)
    if post_range:
        temp_activity = sql_ops.fetch_store_activity(store_id, tomorrow_store_start, end_range)
        activity.extend(temp_activity)
    sql_lock.release()

    num_active_readings , num_inactive_readings = 0 , 0
    num_readings = len(activity)
    # If no readings, return half active, inactive duration
    if num_readings == 0 : return [duration/2, duration/2]
    weightage_of_one_reading = duration / num_readings # duration of one reading/time in between two readings

    for status in activity:
        
        if(status[2] == 'active'):
            num_active_readings += 1
        else :
            num_inactive_readings += 1

    # find active/inactive hours based on number of readings and weightage to every reading
    active_duration = weightage_of_one_reading * num_active_readings
    inactive_duration = weightage_of_one_reading * num_inactive_readings

    return [active_duration, inactive_duration]


def trigger_report_store_wise(report_id, store_id):
    global sql_ops, result, sql_lock, result_lock
    row = StoreReport(store_id)
    sql_lock.acquire(blocking=True)
    timezone_str = sql_ops.fetch_store_timezone(store_id)[0]
    sql_lock.release()
    
    # CALCULATE FOR LAST HOUR
    last_hour = TimingFunctions.get_last_hour()
    curr_hour = TimingFunctions.get_time_now()
    
    [total_active_duration, total_inactive_duration] = calculate_day_wise_activity(store_id, last_hour, timezone_str, last_hour, curr_hour, last_hour=True)

    row.set_uptime_last_hour(total_active_duration)
    row.set_downtime_last_hour(total_inactive_duration)
    

    # CALCULATE FOR LAST DAY
    begin_range = TimingFunctions.get_last_day()
    end_range = TimingFunctions.get_time_now()
    # find number of active hours yesterday & today separately
    [active_hours_day, inactive_hours_day] = calculate_day_wise_activity(store_id, begin_range, timezone_str, begin_range, end_range, False)
    
    total_active_hours = active_hours_day 
    total_inactive_hours = inactive_hours_day 
    row.set_uptime_last_day(total_active_hours)
    row.set_downtime_last_day(total_inactive_hours)

    # CALCULATE FOR LAST WEEK
    begin_range = TimingFunctions.get_last_week()
    end_range = TimingFunctions.get_time_now()

    [active_hours, inactive_hours] = calculate_day_wise_activity(store_id, begin_range, timezone_str, begin_range, None, False)
    total_active_hours = active_hours
    total_inactive_hours = inactive_hours

    next_week_day = TimingFunctions.get_next_day(begin_range)
    count = 1
    while count <= 6:
        [active_duration, inactive_duration] = calculate_day_wise_activity(store_id, next_week_day, timezone_str, None, None, False)
        total_inactive_hours += inactive_duration
        total_active_hours += active_duration
        next_week_day = TimingFunctions.get_next_day(next_week_day)
        count += 1

    [active_duration, inactive_duration] = calculate_day_wise_activity(store_id, next_week_day, timezone_str, None, end_range, False)
    total_active_hours += active_duration
    total_inactive_hours += inactive_duration

    row.set_uptime_last_week(total_active_hours)
    row.set_downtime_last_week(total_inactive_hours)

    # AQUIRE LOCK to update global variable
    result_lock.acquire(blocking=True)
    result[report_id].append(row)
    result_lock.release()

############################

#### PUBLIC FUNCTIONS #####
def trigger_report(report_id: str)->None:
    global result, result_status, sql_ops
    store_ids = sql_ops.fetch_all_stores()
    threads = []
    result[report_id]=[]
    result_status[report_id]=False
    
    for store_id in store_ids:
        new_thread = Thread(target=trigger_report_store_wise, args = (report_id, store_id))
        threads.append(new_thread)
        new_thread.start()

    for thread in threads:
        thread.join()

    result_status[report_id]=True


def get_final_report_status(report_id: str)->bool:
    global result_status
    if report_id not in result_status:
        raise Exception("invalid report id")

    return result_status[report_id]


def deserialize_report(report_id: int) -> pd.DataFrame :
    global result
    data = {}

    data['store_id'] = [report.store_id for report in result[report_id]]
    data['uptime_last_hour(in minutes)'] = [report.uptime_last_hour for report in result[report_id]]
    data['uptime_last_day(in hours)'] = [report.uptime_last_day for report in result[report_id]]
    data['uptime_last_week(in hours)'] = [report.uptime_last_week for report in result[report_id]]
    data['downtime_last_hour(in minutes)'] = [report.downtime_last_hour for report in result[report_id]]
    data['downtime_last_day(in hours)'] = [report.downtime_last_day for report in result[report_id]]
    data['downtime_last_week(in hours)'] = [report.downtime_last_week for report in result[report_id]]

    df = pd.DataFrame(data)
    return df    

############################


### TESTING FUNCTIONS #####
if __name__ == "__main__":
    # trigger_report(1)
    print(TimingFunctions.get_time_now())
###########################