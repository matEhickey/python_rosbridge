# python_rosbridge

Python package to communicate with a rosbridge tcp server asynchronously  
Intended to be use on device that haven't ROS installed  
Originaly developed by Pygmatec for the operatorshift project, to be use on the android Kivy plateform  

Support:
- Topic publishing
- Topic subscribing
- Service calling

## How to use

~~~

from python_rosbridge import RosbridgeParameters, ROS_ServiceCaller, ROS_TopicPublisher

RosbridgeParameters.ip = "10.0.0.129"
RosbridgeParameters.port = 9090

def callbackReceive(recv):
    print("Receive:")
    print(str(recv)+"\n")

def callbackFailure(e):
    print("\nFailure:")
    print(str(e)+"\n")

def callbackReceivePrograms(recv):
    print("Received programs:")
    # print(str(recv)+"\n")
    responseDict = json.loads(recv)
    catString = responseDict["values"]["categories"]
    categories = json.loads(catString)
    pprint(categories)


from random import random
mess = str(random()*1000)

newthread = ROS_ServiceCaller("/operatorshift/programs",callbackReceivePrograms, callbackFailure=callbackFailure,args={}, verbose=True)
# newthread = ROS_ServiceCaller("/rosapi/get_param",callbackReceive,args={"name":"/rosdistro"})
# newthread = ROS_TopicPublisher("/operatorshift/logger","std_msgs/String",'{"data":"'+mess+'"}')

#newthread = ROS_TopicSubscriber("/operatorshift/programs",callbackReceive)  # -> not a topic, a service
# time.sleep(3)
# newthread.unsuscribe()

~~~
