#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

# defines new class MergeArraysNode, extension of Node class
class MergeArraysNode(Node): 

    # constructor
    def __init__(self):
        # calls the super (Node) with node name "merge_arrays_node"
        super().__init__("merge_arrays_node")
        # defines array1 and array2
        self.array1 = None
        self.array2 = None
        # creates two subscriptions to /input/array1 and /input/array2 that will send type Int32MultiArray
        self.subscription1 = self.create_subscription(Int32MultiArray, "/input/array1", self.arr1_callback, 10)
        self.subscription2 = self.create_subscription(Int32MultiArray, "/input/array2", self.arr2_callback, 10)
        # creates publisher that will receive the merged array
        self.publisher = self.create_publisher(Int32MultiArray, "/output/merged_array", 10)    

    # when /input/array1 sends an array, assign array1 and see if its ready to be merged and published
    def arr1_callback(self, msg: Int32MultiArray): 
        self.array1 = msg.data
        self.send_merged_array()
    # when /input/array2 sends an array, assign array2 and see if its ready to be merged and published
    def arr2_callback(self, msg: Int32MultiArray):
        self.array2 = msg.data
        self.send_merged_array()

    # check if both arrays have been initialized, merge them, and publish
    def send_merged_array(self):
        if (self.array1 != None and self.array2 != None):
            self.merged_arr = Int32MultiArray()
            self.merged_arr.data = sorted(self.array1 + self.array2)
            self.publisher.publish(self.merged_arr)
            

def main(args=None):
    # initialize ros2 communication and features
    rclpy.init(args=args)

    merge_arrays_node = MergeArraysNode() #created a node (inhereted from Node class)
    rclpy.spin(merge_arrays_node) # lets node keep running until ctrl+C

    rclpy.shutdown() # destroy the node and shut down ros2 communication

if __name__ == '__main__':
    main()