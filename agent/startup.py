from webservice_helper_method import ip_status, disk_status, all_process_status, network_usage, system_status, \
    memory_status, start_service_remote, service_status, stop_service, agent_list
from flask import Flask
from flask_pymongo import PyMongo
import time,os
from random import randint

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'rar'
app.config['MONGO_URI'] = 'mongodb://test:test123@ds237832.mlab.com:37832/rar'
PATH = 'conf/obj.txt'
mongo = PyMongo(app)
process = mongo.db.processes



def random_with_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)




def create_guid_file():
    if os.path.exists(PATH):
        print("File exists")
        f = open(PATH, 'r')
        print(f.read())
        f.close()

    else:
        print("File doesn't exist")
        f = open(PATH, 'w')
        guid = str(random_with_n_digits(10))
        f.write(guid)
        print(guid)
        f.close()


if __name__ == '__main__':


    create_guid_file()

    while(True):
        print(all_process_status.process_list())
        new_process = all_process_status.process_list()
        process.insert_many(new_process)

        time.sleep(60)






