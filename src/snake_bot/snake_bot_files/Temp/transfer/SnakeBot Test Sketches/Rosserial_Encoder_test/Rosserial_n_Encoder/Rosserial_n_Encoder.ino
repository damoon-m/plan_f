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
#include <ax12.h>


int tst=1;
int cmd[6]={1,1,1,1,1,1};

void messageCb( const std_msgs::Int16& toggle_msg){
  digitalWrite(0, HIGH-digitalRead(0));   // blink the led
  tst=toggle_msg.data;
}

void servo_cmd_Cb(const std_msgs::Int16MultiArray& array){
  for(int i=0;i<8;i++){
    cmd[i]=array.data[i];
    SetPosition(1, msg.data[0]);
  }
}

void messageCb1(const std_msgs::Int64& msg){
  SetPosition(1, msg.data);
  if(msg.data > 1.0)
    digitalWrite(13, HIGH-digitalRead(13));   // blink the led
}


ros::NodeHandle nh;

std_msgs::Int64 msg;

ros::Publisher Encoder("Encoder_Pos", &msg);

ros::Subscriber<std_msgs::Int64> sub_cmd("pos_cmd", &servo_cmd_Cb);



void setup()
{
  nh.initNode();
  nh.advertise(Encoder);

  nh.subscribe(sub_cmd);


  Encoders.Begin();
}

void loop()
{
  msg.data = cmd[tst]*Encoders.right;
  Encoder.publish( &msg );
  nh.spinOnce();
  delay(100);
}


