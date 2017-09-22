# Python package to communicate with a rosbridge tcp server asynchronously
# Intended to be use on device that haven't ROS installed
# Originaly developed by Pygmatec for the operatorshift project, to be use on the android Kivy plateform

import socket
import threading
import time
import json
from pprint import pprint

# PY2 = True
PY2 = False

class _ClientThread(threading.Thread):

    def __init__(self, message, callback=None,timeout=None, singleResponse = False):

        ip="10.0.0.129"
        port=9090

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.callback = callback
        self.timeout = timeout
        self.singleResponse = singleResponse

        self.message = message if(PY2) else message.encode("utf-8")

        print("Message: "+str(message))

        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start()

    def run(self):

        self.clientsocket.connect((self.ip, self.port))
        print("Connection: %s %s" % (self.ip, self.port ))

        self.clientsocket.send(self.message)

        if(self.callback):
            if(self.timeout):
                self.clientsocket.settimeout(self.timeout)

            self.do_run = True
            while(self.do_run):
                r = self.clientsocket.recv(2048).decode("utf-8")
                if(not r == "") : self.callback(r)# if(r is not None) else pass
                if(self.singleResponse):
                    self.do_run = False


        self.clientsocket.close()

class ROS_TopicPublisher(_ClientThread):
    def __init__(self,topic,type,msg):
        super(ROS_TopicPublisher,self).__init__('{"op":"publish","topic":"'+topic+'","msg":'+msg+'}')

class ROS_TopicSubscriber(_ClientThread):
    def __init__(self,topic,callback):
        super(ROS_TopicSubscriber,self).__init__('{"op":"subscribe","topic":"'+topic+'"}',callback=callback)
    def unsuscribe(self):
        self.do_run = False
        self.clientsocket.shutdown(socket.SHUT_WR)

class ROS_ServiceCaller(_ClientThread):
    def __init__(self,service,callback, args=None):
        arguments = "" if args is None else ',"args":'+json.dumps(args)#str(args).replace("'","\"")
        print("arguments: '"+arguments+"'")
        super(ROS_ServiceCaller,self).__init__('{"op":"call_service","service":"'+service+'"'+arguments+'}',callback=callback, singleResponse=True)

if(__name__=="__main__"):

    def callbackReceive(recv):
        print("\n\nReceive:")
        print(str(recv)+"\n")

    def callbackReceivePrograms(recv):
        print("\n\nReceive programs:")
        # print(str(recv)+"\n")
        responseDict = json.loads(recv)
        catString = responseDict["values"]["categories"]
        categories = json.loads(catString)
        pprint(categories)


    from random import random
    mess = str(random()*1000)

    newthread = ROS_ServiceCaller("/operatorshift/programs",callbackReceivePrograms)
    # newthread = ROS_ServiceCaller("/rosapi/get_param",callbackReceive,args={"name":"/rosdistro"})
    # newthread = ROS_TopicPublisher("/operatorshift/logger","std_msgs/String",'{"data":"'+mess+'"}')

    #newthread = ROS_TopicSubscriber("/operatorshift/programs",callbackReceive)  # -> not a topic, a service
    # time.sleep(3)
    # newthread.unsuscribe()

    # newthread = _ClientThread("Test\n")

    print("end")
