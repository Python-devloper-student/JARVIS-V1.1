#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>
Adafruit_SSD1306 display(128,64,&Wire,-1);
void setup() {
Wire.begin();
display.begin(SSD1306_SWITCHCAPVCC,0X3C);
Serial.begin(9600);\
display.clearDisplay();
display.display();

}

void loop() {
if (Serial.available()){
 String data=Serial.readStringUntil('<');
 while(data=="listening"){
 face(34,30,94,14,"~~~~");
 display.setCursor(10, 2);
 display.setTextColor(WHITE);
 display.print("listening");
 display.display();
  if (Serial.available()){
    data=Serial.readStringUntil('<');
  }
  else{data="listening";}
  if (data!="listening"){break;}
 }
  while (data=="speak"){
face(34,30,94,14,"~~~~");
delay(300);
face(34,30,94,14,"\\__/");
delay(300);
if (Serial.available()){
data=Serial.readStringUntil('<');}
else {data="speak";}
 if(data!="speak"){break;}
  }
  
while (data=="thinking"){
  face(34,30,94,10,"|----|");
  delay(300);
  face(34,25,94,10,"~~~~");
  delay(300);
  face(34,35,94,10,"~~~~");
  delay(300);
  if (Serial.available()){
data=Serial.readStringUntil('<');}
else {data="thinking";}

 if(data!="thinking"){break;}
}
while (data=="ide"){
  display.clearDisplay();
  display.fillCircle(35, 35 ,10,WHITE);
  display.fillCircle(83, 35,10, WHITE);
  display.fillCircle(88, 35,4, BLACK);
  display.fillCircle(40, 35 ,4,BLACK);
  display.setCursor(55, 47);
  display.print("~~~~");
  display.display();
delay(300);
  display.clearDisplay();

  display.setCursor(64, 32);
  display.fillCircle(40, 35 ,10,WHITE);
  display.fillCircle(88, 35,10, WHITE);
  display.fillCircle(88, 35,4, BLACK);
  display.fillCircle(40, 35 ,4,BLACK);
  display.setCursor(55, 47);
  display.print("\\__/");
display.display();

delay(300);

display.clearDisplay();

  display.fillCircle(45, 35 ,10,WHITE);
  display.fillCircle(93, 35,10, WHITE);
  display.fillCircle(88, 35,4, BLACK);
  display.fillCircle(40, 35 ,4,BLACK);
  display.setCursor(55, 47);
  display.print("~~~~");

display.display();

delay(300);
  if (Serial.available()){
data=Serial.readStringUntil('<');}
else {data="ide";}
 if(data!="ide"){break;}
}}
}

void face(int eyesx,int eyesy,int leyesx,int eyesr,String  mounth){
  display.clearDisplay();
  display.fillCircle(eyesx, eyesy,eyesr,WHITE);
    display.fillCircle(eyesx, eyesy,4,BLACK);
  display.fillCircle(leyesx, eyesy, eyesr, WHITE);
   display.fillCircle(leyesx, eyesy, 4, BLACK);
   display.setCursor(55, 50);
   display.setTextColor(WHITE);
   display.print(mounth);
  display.display();
}