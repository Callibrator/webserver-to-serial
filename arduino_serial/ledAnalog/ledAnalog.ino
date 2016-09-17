//led analog

int volume = 100;
int ledPin = 3;
char buffer[1024];
int newVolume=100;

char haveData = 0;

void setup()
{
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
  
}

void loop()
{
  haveData =0;
  //reset buffer
  for(int i=0;i<1024;i++)
    buffer[i] = '\0';
    
  for(int i =0;i<1023;i++){
    if(Serial.available() > 0){
      buffer[i] = Serial.read();
      haveData = 1;
    }
    else
      break;
  }
  if(haveData){
     if(strstr(buffer,"volume=")){
       char *pos = strstr(buffer,"volume=");
       pos += strlen("volume=");
       char integer[4];
       for(int i=0;i<3;i++){
         integer[i] = *pos;
         pos++;  
       }
       integer[3] = '\0';
       int temp=atoi(integer);
       newVolume=temp;
       if(temp > 255)
           newVolume = 255;
       if(temp < 0)
           newVolume = 0;
       
    }
    if(strstr(buffer,"whatvolume")){
        Serial.print(newVolume); 
    }
  }
  do{
    analogWrite(ledPin,volume);
    if(volume < newVolume){
      volume++; 
    }else if(volume > newVolume){
      volume--; 
    }
    delay(10);
  }while(volume != newVolume);
  delay(1000);
  
}
