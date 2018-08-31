import sys

sys.path += [".."]
from webservice_helper_method import ip_status, disk_status, all_process_status, network_usage, system_status, \
    memory_status, start_service_remote, service_status, agent_list
from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo
import time, os
from random import randint
from threading import Thread

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'rar'
app.config['MONGO_URI'] = 'mongodb://admin:novell@54.68.243.229/rar'
mongo = PyMongo(app)

conn = MongoClient()
db = conn.rar

ip_collection = mongo.db.IP
disk_collection = mongo.db.DISK
network_collection = mongo.db.NETWORK
memory_collection = mongo.db.MEMORY
system_collection = mongo.db.SYSTEM
service_collection = mongo.db.SERVICE
process_collection = mongo.db.PROCESS


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def create_guid_file():
    global guid_con
    if os.path.exists(r"C:\Users\user\Downloads\RAR\agent" + os.sep + "guid.txt"):
        print("File exists")
        f = open(r"C:\Users\user\Downloads\RAR\agent" + os.sep + "guid.txt", 'r')
        guid_con = f.read().strip()
        print(f.read())
        f.close()

    else:
        print("File doesn't exist")
        f = open(r"C:\Users\user\Downloads\RAR\agent" + os.sep + "guid.txt", 'w')
        guid = str(random_with_n_digits(10))
        f.write(guid)
        print(guid)
        f.close()


def initialize():
    # guid creation
    create_guid_file()
    # ip push
    json_response_ip = ip_status.get_ip()
    ip_collection.insert(json_response_ip)
    # network push
    json_response_network = network_usage.get_network()
    network_collection.insert(json_response_network)
    # memory push
    json_response_memory = memory_status.get_memory_usage()
    memory_collection.insert(json_response_memory)
    # system push
    json_response_system = system_status.system_status()
    system_collection.insert(json_response_system)
    # service push
    json_response_service = service_status.service_list()
    service_collection.insert(json_response_service)
    # process push
    json_response_process = all_process_status.process_list()
    process_collection.insert(json_response_process)


def m1():
    app.run()


def m2():
    while True:
        # ip push
        json_response_ip = ip_status.get_ip()
        # command_ip = "{'guid':" + guid_con + "},{'$set':" + str(json_response_ip) + "}"
        ip_collection.update({'guid': guid_con}, {'$set': json_response_ip})

        # network push
        json_response_network = network_usage.get_network()
        # command_network = "{'guid':" + guid_con + "},{$set:" + str(json_response_network) + "}"
        network_collection.update({'guid': guid_con}, {'$set': json_response_network})

        # memory push
        json_response_memory = memory_status.get_memory_usage()
        # command_memory = "{'guid':" + guid_con + "},{$set:" + str(json_response_memory) + "}"
        memory_collection.update({'guid': guid_con}, {'$set': json_response_memory})

        # system push
        json_response_system = system_status.system_status()
        # command_system = "{'guid':" + guid_con + "},{$set:" + str(json_response_system) + "}"
        system_collection.update({'guid': guid_con}, {'$set': json_response_system})

        # service push
        json_response_service = service_status.service_list()
        # command_service = "{'guid':" + guid_con + "},{$set:" + str(json_response_service) + "}"
        service_collection.update({'guid': guid_con}, {'$set': json_response_service})
        # process push

        json_response_process = all_process_status.process_list()
        # command_process = "{'guid':" + guid_con + "},{$set:" + str(json_response_process) + "}"
        process_collection.update({'guid': guid_con}, {'$set': json_response_process})

        time.sleep(randint(0, 30))


if __name__ == '__main__':
    initialize()
    t1 = Thread(target=m1)
    t2 = Thread(target=m2)
    t1.start()
    t2.start()
