import datetime

count = 1

def cleanup_backlogs():
    file = open("server_log.log", "w")
    file.write("")
    file.close()

class Server:
    """A simulated server which provides data to clients through requests and thus multiple clients of same
    IP addresses and thus can also flood the servers"""
    users = []
    def __init__(self, user_list = []):
        """It takes an optional parameter which can be used to initialize a server
        by providing initial connections"""
        global count
        self.id = count
        count += 1
        self.users += user_list
        with open("server_log.log", "a") as log_file:
            log_file.write("{} - INFO: NEW INSTANCE Server[{}] msg =  (a new server instance was created)\n".format(datetime.datetime.now(), self.id))
            log_file.close()

    def log(self, log_type, details, msg = "None"):
        with open("server_log.log", "a") as log_file:
            log_file.write("{} - {}: {} AT Server[{}] msg =  ({})\n".format(datetime.datetime.now(), log_type.upper(), details.upper(), self.id, msg))
            log_file.close()

    def add_connection(self, users):
        """It takes users parameter as a dictionary of users and the number of connections to an IP
        as its value"""
        for user in users:
            if self.get_load() < 500:
                self.users.append(user)
                self.log("info", "added connection", "IP: {}, Load: {}".format(user, self.get_load()))
            else:
                self.log("error", "on heavy load", "IP: {} can't be connected !".format(user))

    def remove_connection(self, connections):
        for connection in connections:
            if connection in self.users:
                self.users.remove(connection)
                self.log("info", "removed connection", "IP: {}, Load: {}".format(connection, self.get_load()))

    def get_load(self):
        return len(self.users)

    def __str__(self):
        return "Server with id: {}".format(self.id)

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
    print(server.get_load(), server.users)
