/*
 * rosserial Publisher Example
 * Prints "hello world!"
 */

// Use the following line if you have a Leonardo or MKR1000
//#define USE_USBCON

#include <ros.h>
#include <vector>
#include <std_msgs/Int64.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Empty.h>

#include "std_msgs/MultiArrayLayout.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/Int16MultiArray.h"

#include <EncodersAB.h>
int tst=1;
int cmd[8]={
  1,1,1,1,1,1,1,1};

void messageCb( const std_msgs::Int16& toggle_msg){
  digitalWrite(0, HIGH-digitalRead(0));   // blink the led
  tst=toggle_msg.data;
}

void servo_cmd_Cb(const std_msgs::Int16MultiArray& array){
  for(int i=0;i<8;i++){
    cmd[i]=array.data[i];
  } 
}

ros::NodeHandle nh;

std_msgs::Int64 msg;

ros::Publisher Encoder("Encoder_Pos", &msg);

ros::Subscriber<std_msgs::Int16> sub1("toggle_led", &messageCb );
ros::Subscriber<std_msgs::Int16MultiArray> sub("servo_input", &servo_cmd_Cb );


void setup()
{
  nh.initNode();
  nh.advertise(Encoder);

  nh.subscribe(sub);
  nh.subscribe(sub1);


  Encoders.Begin();
}

void loop()
{
  msg.data = cmd[tst]*Encoders.right;
  Encoder.publish( &msg );
  nh.spinOnce();
  delay(100);
}


