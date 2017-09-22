# python-rosbridge

Python package to communicate with a rosbridge tcp server asynchronously  
Intended to be use on device that haven't ROS installed  
Originaly developed by Pygmatec for the operatorshift project, to be use on the android Kivy plateform  

Support:
- Topic publishing
- Topic subscribing
- Service calling

## How to use

~~~
def callbackReceive(recv):
    print("\n\nReceive:")
    print(str(recv)+"\n")

def callbackReceivePrograms(recv):
    print("\n\nReceive programs:")
    # print(str(recv)+"\n")
    responseDict = json.loads(recv)
    catString = responseDict["values"]["categories"]
    categories = json.loads(catString)

    from pprint import pprint
    pprint(categories)

newthread = ROS_ServiceCaller("/operatorshift/programs",callbackReceivePrograms)
# newthread = ROS_ServiceCaller("/rosapi/get_param",callbackReceive,args={"name":"/rosdistro"})
# newthread = ROS_TopicPublisher("/operatorshift/logger","std_msgs/String",'{"data":"'+mess+'"}')
~~~
