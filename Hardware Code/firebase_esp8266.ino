
#include <ESP8266Firebase.h>
#include <ESP8266WiFi.h>

// Update these with values suitable for your network.

const char* ssid = "Esptest";
const char* password = "testesp123";
#define REFERENCE_URL "https://wireless-train-signalization-default-rtdb.europe-west1.firebasedatabase.app/"  // Your Firebase project reference url

Firebase firebase(REFERENCE_URL);

int outpin = 2;
int warningpin = 0;


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
//  Serial.println();
//  Serial.print("Connecting to ");
//  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
//    Serial.print(".");
  }

//  Serial.println("");
  digitalWrite(outpin, HIGH);
  Serial.println("verified");
//  Serial.println("IP address: ");
//  Serial.println(WiFi.localIP());
}




void setup() {
  pinMode(outpin, OUTPUT);  
  pinMode(warningpin, OUTPUT);
  Serial.begin(115200);
  setup_wifi();

}

void loop() {

if (WiFi.status() != WL_CONNECTED) {
  digitalWrite(outpin, LOW);
  setup_wifi();
  }


 String incomingData;
 if (Serial.available() > 0) {
    digitalWrite(outpin, LOW);

    
    incomingData = Serial.readString();

    if (incomingData.indexOf("connect") != -1){
      if(WiFi.status() == WL_CONNECTED){
        Serial.println("verified");
        digitalWrite(outpin, HIGH);
        }
      else{ 
        setup_wifi();}
      }
    
    // say what you got:
//    Serial.print("I received: ");
//    Serial.println(incomingData);
 

    else{
    incomingData.trim();
    //Serial.print("I received: ");
    //Serial.println(incomingData);
    int response = firebase.pushString("data", incomingData);
    if (response == 200){
    Serial.println("sent");}
    else if (response == 400){
    Serial.println("failed");}
    digitalWrite(outpin, HIGH);
    }

   /*
    String warningdata = firebase.getString("warning");
    if (warningdata.indexOf("Warning") != -1){
      digitalWrite(warningpin, HIGH);
      }
    else{
      digitalWrite(warningpin, LOW);
    }
    digitalWrite(outpin, HIGH);


    */
    }
  

  
 }
   
