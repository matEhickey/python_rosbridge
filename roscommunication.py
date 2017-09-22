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

    def __init__(self, message, callbackSuccess=None, callbackFailure=None,timeout=None, singleResponse = False):

        ip="10.0.0.128"
        port=9090

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.callbackSuccess = callbackSuccess
        self.callbackFailure = callbackFailure
        self.timeout = timeout
        self.singleResponse = singleResponse

        self.message = message if(PY2) else message.encode("utf-8")

        print("Message: "+str(message))

        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start()

    def run(self):
        try:
            self.clientsocket.connect((self.ip, self.port))
        except Exception as e:
            if(self.callbackFailure):
                self.callbackFailure(e)
            else:
                print("Socket connection failure : "+str(e))
            return
        print("Connection: %s %s" % (self.ip, self.port ))


        try:
            self.clientsocket.send(self.message)
        except Exception as e:
            if(self.callbackFailure):
                self.callbackFailure(e)
            else:
                print("Socket send failure"+str(e))
            return


        if(self.callbackSuccess):
            if(self.timeout):
                self.clientsocket.settimeout(self.timeout)

            self.do_run = True
            while(self.do_run):
                r = None
                try:
                    r = self.clientsocket.recv(2048).decode("utf-8")
                except Exception as e:
                    if(self.callbackFailure):
                        self.callbackFailure(e)
                    else:
                        print("Socket receive failure"+str(e))
                    return


                if(not r == "") : self.callbackSuccess(r)# if(r is not None) else pass
                if(self.singleResponse):
                    self.do_run = False


        self.clientsocket.close()



class ROS_TopicPublisher(_ClientThread):
    def __init__(self,topic,type,msg, callbackFailure=None):
        super(ROS_TopicPublisher,self).__init__('{"op":"publish","topic":"'+topic+'","msg":'+msg+'}')

class ROS_TopicSubscriber(_ClientThread):
    def __init__(self,topic,callback, callbackFailure=None):
        super(ROS_TopicSubscriber,self).__init__('{"op":"subscribe","topic":"'+topic+'"}',callbackSuccess=callback)
    def unsuscribe(self):
        self.do_run = False
        self.clientsocket.shutdown(socket.SHUT_WR)

class ROS_ServiceCaller(_ClientThread):
    def __init__(self,service,callback, args=None, callbackFailure=None):
        arguments = "" if args is None else ',"args":'+json.dumps(args)#str(args).replace("'","\"")
        print("arguments: '"+arguments+"'")
        super(ROS_ServiceCaller,self).__init__('{"op":"call_service","service":"'+service+'"'+arguments+'}',callbackSuccess=callback, callbackFailure=callbackFailure, singleResponse=True)



if(__name__=="__main__"):

    def callbackReceive(recv):
        print("\n\nReceive:")
        print(str(recv)+"\n")

    def callbackFailure(e):
        print("\n\Failure:")
        print(str(e)+"\n")

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
