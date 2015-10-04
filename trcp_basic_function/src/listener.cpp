#include "std_msgs/String.h"
#include "ros/ros.h"

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
  
  char ccc[128];
  strcpy(ccc, msg->data.c_str());
  printf("MSG:%s\n",ccc);

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;

 ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);
 ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter2", 1000);
  ros::spinOnce();

ros::Rate loop_rate(10);
while(ros::ok())
{
printf("AAAAAAAAAAAAAAAAAAAAA\n");
    std_msgs::String msg;

    std::string sss="return";
    msg.data = sss;

    chatter_pub.publish(msg);
    ros::spinOnce();


  loop_rate.sleep();
}

  return 0;
}
