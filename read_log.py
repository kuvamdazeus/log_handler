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
            returned_dict["Activities"] = dict[ip]
        returned_list.append(returned_dict)

    file = open("report.txt", "w")
    writer = csv.DictWriter(file, ["IP", "Activities"])
    writer.writeheader()
    writer.writerows(returned_list)
    file.close()
    return returned_list

def investigate_error_and_info(file_path):
    """returns a list of tuples and tuple = (date, detail, message)"""
    detail_pattern = r":\s?([A-Z\s]+)\s?AT"
    message_pattern = r"\((.*)\)"
    date_pattern = r"^([0-9\-\s\:]+)\."
    file = open(file_path)
    error_lines = []
    info_lines = []
    for line in file:
        tuple = (re.search(date_pattern, line).group(1), re.search(detail_pattern, line).group(1).strip(), re.search(message_pattern, line).group(1))
        if "ERROR" in line:
            error_lines.append(tuple)
        elif "INFO" in line:
            info_lines.append(tuple)
    file.close()
    return error_lines, info_lines

def write_error_and_info(investigated_error_and_info):
    error_lines, info_lines = investigated_error_and_info
    file = open("report.txt", "a")
    file.write("-"*50 + "\n")
    file.write("ERRORS: \n")
    error_list = []
    info_list = []
    if len(error_lines) > 0:
        for error_tuple in error_lines:
            error_dict = {}
            date, detail, message = error_tuple
            error_dict["Date"] = date
            error_dict["Details"] = detail
            error_dict["Message"] = message
            error_list.append(error_dict)
        writer = csv.DictWriter(file, ["Date", "Details", "Message"])
        writer.writeheader()
        writer.writerows(error_list)
    else:
        file.write("None\n")
    file.write("-"*50 + "\n")
    file.write("INFO: \n")
    if len(info_lines) > 0:
        for info_tuple in info_lines:
            info_dict = {}
            date, detail, message = info_tuple
            info_dict["Date"] = date
            info_dict["Details"] = detail
            info_dict["Message"] = message
            info_list.append(info_dict)
        writer = csv.DictWriter(file, ["Date", "Details", "Message"])
        writer.writeheader()
        writer.writerows(info_list)
    else:
        file.write("None\n")
    file.close()

process_log_file("server_log.log", "added connection")
write_error_and_info(investigate_error_and_info("server_log.log"))
