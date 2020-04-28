#! /usr/bin/env python3
import datetime
# self.log("error", "on heavy load", "IP: {} can't be connected !".format(user))
count = 1

def cleanup_backlogs():
    file = open("server_log.log", "w")
    file.write("")
    file.close()

class Server:
    """A simulated server which provides data to clients through requests and thus multiple clients of same
    IP addresses and thus can also flood the servers"""
    def remove_connection(self, connections):
        if type(connections) is list:
            for connection in connections:
                if connection in self.users:
                    self.users.remove(connection)
                    self.log("info", "removed connection", "IP: {}, Load: {}".format(connection, self.get_load()))
        else:
            if connections in self.users:
                self.users.remove(connections)
                self.log("info", "removed connection", "IP: {}, Load: {}".format(connections, self.get_load()))


    def add_connection(self, users):
        """It takes users parameter as a dictionary of users and the number of connections to an IP
        as its value"""
        if self.get_load() > 500:
            self.log("error", "heavy load")
            return "Error"
        if type(users) is list:
            for user in users:
                if not user in self.users:
                    self.users.append(user)
                    self.log("info", "added connection", "IP: {}, Load: {}".format(user, self.get_load()))
        else:
            if not users in self.users:
                self.users.append(users)
                self.log("info", "added connection", "IP: {}, Load: {}".format(users, self.get_load()))

    def __init__(self, user_list = []):
        self.users = []
        """It takes an optional parameter which can be used to initialize a server
        by providing initial connections"""
        global count
        self.id = count
        count += 1
        if len(user_list) > 0:
            for user in user_list:
                self.add_connection(user)
        with open("server_log.log", "a") as log_file:
            log_file.write("{} - INFO: NEW INSTANCE AT Server[{}] msg =  (a new server instance was created)\n".format(datetime.datetime.now(), self.id))
            log_file.close()

    def log(self, log_type, details, msg = "None"):
        with open("server_log.log", "a") as log_file:
            log_file.write("{} - {}: {} AT Server[{}] msg =  ({})\n".format(datetime.datetime.now(), log_type.upper(), details.upper(), self.id, msg))
            log_file.close()

    def get_load(self):
        return len(self.users)

    def __str__(self):
        return "Server[{}]".format(self.id)

    def transfer(self, other, user_number):
        """Defines a new server and transfers users in the self server to the specified server"""
        try:
            assert user_number <= self.get_load()
        except AssertionError:
            return None
        other.add_connection(self.users[:user_number])
        self.remove_connection(self.users[:user_number])

if __name__ == "__main__":
    """adding new connections to create logs that need to be extracted"""
    cleanup_backlogs()
    server = Server()
    server.add_connection(["190.189.23.34", "190.189.23.34"])
    server.add_connection(["127.0.0.1", "127.0.0.1", "198.145.233.34", "172.20.10.5"])
    server.add_connection(["145.534.67.0", "190.65.9.23"])
    server.add_connection(["145.534.67.0", "190.65.9.23"])
    server.add_connection(["127.0.0.1", "127.0.0.1", "198.145.233.34", "172.20.10.5"])
    server.add_connection(["145.534.67.0", "190.65.9.23"])
    server.add_connection(["127.0.0.1", "127.0.0.1", "198.145.233.34", "172.203.102.55"])
    server.add_connection(["127.0.0.1", "127.0.0.1", "198.145.233.34", "172.20.10.5"])
    server.add_connection(["190.189.23.34", "190.189.23.34"])
    server.remove_connection(["127.0.0.1", "127.0.0.1", "198.145.233.34", "172.20.10.5"])
    server.add_connection(["124.645.34.9", "189.554.78.8", "132.87.89.90", "172.20.10.5"])
    server1 = Server()
    server.transfer(server1, 3)
    print(server.get_load(), server.users)
    print(server1.users, server1.get_load())
