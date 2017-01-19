#! /usr/bin/env python
import rospy
from Ros_Coms.msg import bbox,bbox_array
from std_msgs.msg import String, Header
from bbox.srv import *
class SpacialCommander :
    def __init__(self,topic="inboxes"):
        self.input = rospy.resolve_name( topic )
        self.input = self.input if self.input != ("/"+topic) else "/darknet_bboxes";
        self.out   = rospy.resolve_name( "outcmds" )
        self.out   = self.out if self.out != "/outcmds" else "/spacial_correction"
        print ( "bbox topic: ", self.input )
        print ( "cmdo topic: ", self.out   )
        self.differential = 0;
        self.service = None
    def onReceiveMsg(self):
        def onBoxes(boxarray):
            width = 320
            if len(boxarray.bboxes) > 0:
                bbox = boxarray.bboxes[0]
                #calc offset from center
                offset =  (((bbox.xmin + bbox.xmax)/2) - width/2)
                # give a tolerance of 15pix (integer division)
                self.differential = offset/15
            else:
                self.differential = 0
        return onBoxes

    def get_diff(self):
        def return_diff():
            retval = self.differential
            self.differential = 0
            return retval
        return return_diff
    
    def start(self):
        rospy.init_node("differential_service")
        rospy.Subscriber(self.input, bbox_array, self.onReceiveMsg())
        self.Service  = rospy.Service('get_diff', Movement, self.get_diff())
        rospy.spin()
        
#This will be a test node that
#runs on the assumption that there will only be
#a single person in the frame
#and will attempt to "follow" them
def main():
    sc = SpacialCommander()
    sc.start()


if __name__ == '__main__':
    main()
