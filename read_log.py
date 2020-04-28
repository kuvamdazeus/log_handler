#! /usr/bin/env python3
import re, operator, csv
"""This script reads the server_log.py and extracts the ip addresses which added or established a connection
with the server, process_log_file() function takes the log_file as its first argumnet and the details of the
info or error message and then searches the log_file to extract the ip addresses associated with number of requests"""
def process_log_file(log_file, details):
    details = details.strip().upper().split()

    ip_pattern = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    detail_pattern = r": ([A-Z\s]+) AT"

    user_dict = {}

    file = open(log_file)

    for line in file:
        ip = re.search(ip_pattern, line)
        if ip != None:
            ip = ip.group()
            user_dict[ip] = user_dict.get(ip, 0) + 1
    file.close()

    sorted_tuple_list = sorted(user_dict.items(), key = operator.itemgetter(1), reverse = True)
    result_list = []
    for tuple in sorted_tuple_list:
        dict = {}
        ip, number = tuple
        dict[ip] = number
        result_list.append(dict)

    returned_list = []
    for dict in result_list:
        returned_dict = {}
        for ip in dict:
            returned_dict["IP"] = ip
            returned_dict["Number"] = dict[ip]
        returned_list.append(returned_dict)

    file = open("report.txt", "w")
    writer = csv.DictWriter(file, ["IP", "Number"])
    writer.writeheader()
    writer.writerows(returned_list)
    file.close()



process_log_file("server_log.log", "added connection")
