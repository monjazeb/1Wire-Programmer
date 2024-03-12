#include <OneWire.h>
#include <LiquidCrystal.h>

//=================================================== Hardware Setup

//------------------------------------------ Push button pin ( /SW )
#define SW 53
//--------------------------------------------- 1Wire and /PROG pins
#define WIRE 5
#define PROG 6
//--------------------------------------- Read, Write and Error LEDS
#define L_READ A8
#define L_WRITE A9
#define L_ERROR A10
//----------------------------------------- 16x2 LCD Connection Pins
#define D4 10
#define D5 9
#define D6 8
#define D7 7
#define EN 11
#define RS 12
//---------------------------------------------- EEPROM Program pins
#define WE 23
#define OE 37
#define CE 41
//------------------------------------- EEPROM Address and data pins
#define LEN_ADDR_PINS 19
const uint8_t addr_pins[] = {44, 42, 40, 38, 36, 34, 32, 30, 31, 33, 39, 35, 28, 29, 27, 26, 24, 25, 22};
const uint8_t data_pins[] = {46, 48, 50, 51, 49, 47, 45, 43};
//-------------------------------------------------------- Constants
#define NOP __asm__ __volatile__ ("nop\n\t")
#define block_size 32
#define TIMEOUT 20000
String buses[2] = {"EEPROM", "1Wire "};
//------------------------------------------------- Global Variables
uint16_t mem_chunks = 256;
bool error = 0;
uint8_t bus = 0;
uint8_t chip = 0;
uint8_t buf[block_size+3];
uint8_t addr[8];
char command[2];

//======================================================= Initialize
OneWire hub(WIRE);
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);
//------------------------------------------------------------ Setup
void setup() {
  //---------------------------------------------- Pin Mode settings
  pinMode(SW, INPUT_PULLUP);

  pinMode(PROG, OUTPUT);
  digitalWrite(PROG, HIGH);

  pinMode(WE, OUTPUT);
  pinMode(OE, OUTPUT);
  pinMode(CE, OUTPUT);
  digitalWrite(WE, HIGH);
  digitalWrite(OE, HIGH);
  digitalWrite(CE, LOW);

  pinMode(L_READ, OUTPUT);
  pinMode(L_WRITE, OUTPUT);
  pinMode(L_ERROR, OUTPUT);
  digitalWrite(L_ERROR, HIGH);
  delay(200);
  digitalWrite(L_WRITE, HIGH);
  delay(200);
  digitalWrite(L_READ, HIGH);
  delay(200);
  digitalWrite(L_ERROR, LOW);
  digitalWrite(L_READ, LOW);
  digitalWrite(L_WRITE, LOW);

  set_addr_pins_output();
  set_data_pins(INPUT);

  Serial.setTimeout(500);
  Serial.begin (115200);
  lcd.begin(16, 2);
  print_lcd(0, 0, "*ARM Programmer*");
  print_lcd(0, 1, "Connecting...   ");
  digitalWrite(L_ERROR, HIGH);

  while (true) {
    while (!Serial.available()){
      digitalWrite(L_READ, !digitalRead(L_READ));
      delay(200);
      digitalWrite(L_WRITE, !digitalRead(L_WRITE));
      delay(200);
    }
    if (Serial.read() == 'C') {
      digitalWrite(L_ERROR, LOW);
      digitalWrite(L_READ, LOW);
      digitalWrite(L_WRITE, LOW);
      print_lcd(0, 0, "Chip:      ");
      print_lcd(10, 0, buses[bus]);
      print_lcd(0, 1, "Connected.      ");
      Serial.print('>');
      break;
    }
  }
}

//======================================================== Main Loop
void loop() {
  while(!Serial.available());
  digitalWrite(L_ERROR, LOW);
  if(Serial.read() == ':'){
    Serial.readBytes(command, 1);
    run_command();
  }
  if (digitalRead(SW) == LOW) {
    digitalWrite(L_READ, HIGH);
    delay(1000);
    digitalWrite(L_READ, LOW);
  }
}

void print_lcd(uint8_t x, uint8_t y, String text) {
  lcd.setCursor(x, y);
  lcd.print(text);
}

void run_command() {
  switch (command[0]) {
    case 'C': {
        Serial.print(">");
        break;
      }
    case 'S': {
        Serial.readBytes(command, 1);
        if (command[0] == 'R') {
          bus = 0;
        }
        if (command[0] == '1') {
          bus = 1;
        }
        print_lcd(0, 0, "Chip:     ");
        print_lcd(10, 0, buses[bus]);
        Serial.print(":");
        Serial.println(bus,HEX);
        break;
      }
    case 'R': {
        print_lcd(0, 1, "Reading...      ");
        digitalWrite(L_READ, HIGH);
        switch (bus) {
          case 0: {
              read_rom(mem_chunks);
              break;
            }
          case 1: {
              read_1wire(mem_chunks);
              break;
            }
        }
        digitalWrite(L_READ, LOW);
        print_lcd(10, 1, ".Done.");
        break;
      }
    case 'W': {
        print_lcd(0, 1, "Writing...      ");
        digitalWrite(L_WRITE, HIGH);
        switch (bus) {
          case 0: {
              write_rom();
              break;
            }
          case 1: {
              write_1wire();
              break;
            }
        }
        digitalWrite(L_WRITE, LOW);
        print_lcd(10, 1, ".Done.");
        break;
      }
    case 'M': {
      String parms = Serial.readString();
      mem_chunks = parms.toInt();
      print_lcd(0, 1, "Size:           ");
      print_lcd(6, 1, String(block_size));
      print_lcd(10, 1, "x");
      print_lcd(11, 1, String(mem_chunks));
      
      Serial.println(mem_chunks, HEX);
      break;
    }
    case 'E': {  // ----------------------- command E: Erase EEPROM
      if (bus==0) {
        print_lcd(0, 1, "*Erasing EEPROM*");
        eraseChip();
        print_lcd(0, 1, "EEPROM Erased.  ");
        break;
      }
    }
    case 'T': {
      // write_byte(0,'A');
      // Serial.write(read_byte(0));
      // Serial.print('=');
      // write_byte(0,'M');
      // Serial.write(read_byte(0));
      // Serial.println();
      break;
    }
    default : {
      digitalWrite(L_ERROR, HIGH);
      while(Serial.available()) Serial.read();
      break;
    }
  }
}

bool find_1wire() {
  byte leemem[3] = {0xF0 , 0x00 , 0x00};
  byte ccrc;
  byte ccrc_calc;

  if (!hub.reset()){
    print_lcd(6, 0, "Not found!");
    Serial.print("x");
    return false;
  }
  hub.reset_search();
  if(!hub.search(addr)){
    print_lcd(6, 0, "No device!");
    Serial.print("x");
    return false;
  }
  if (OneWire::crc8(addr,7) != addr[7]){
    print_lcd(6,0,"CRC Error!");
    return false;
  }
  print_lcd(6, 0, "1WireFound");
  chip = addr[0];
  Serial.println(chip);
  return true;
}

void read_1wire(uint16_t ch) {
  int retry = 0;
  while (!find_1wire()){
    if (retry > 10) {
      digitalWrite(L_ERROR,HIGH);
      error = true;
      break;
    }
    retry++;
    delay(3000);
  }
  uint16_t chunks;
  if (!error) {
    if (chip) {
      chunks = ch;
      hub.write(0xF0 , 1);
      hub.write(0x00 , 1);
      hub.write(0x00 , 1);
      while (chunks) {
        hub.read_bytes(buf, block_size);
        Serial.write(buf, block_size);
        chunks--;
        if (error) break;
      }
    }
  }
  Serial.print('.');
}

void write_1wire() {
  int retry = 0;
  uint8_t d;
  uint8_t crc_buf[3];
  while (!find_1wire()){
    if (retry > 10) {
      digitalWrite(L_ERROR,HIGH);
      error = true;
      break;
    }
    retry++;
    delay(3000);
  }
  uint16_t a = 0;
  if (!error) {
    if (chip) {
      while (Serial.available() <=0); // wait for serial to start sending
      hub.write(0xF3 , 1);
      hub.write(0x00 , 1);
      hub.write(0x00 , 1);
      while (Serial.available() > 0) {
        d = Serial.read();
        crc_buf[0]=a & 0xff;
        crc_buf[1]=a >> 8;
        crc_buf[2]=d;

        hub.write(d, 1);
        // Serial.print(d, HEX);
        // Serial.print(" crc:");
        // Serial.print(OneWire::crc16(crc_buf, 3), HEX);
        // Serial.print(":");
        // Serial.print(hub.check_crc16(crc_buf, 3), HEX);
        if (true){ // OneWire::crc16(crc_buf, 3) == hub.read()
          digitalWrite(PROG,LOW);
          delay(1);
          digitalWrite(PROG,HIGH);
          delay(1);
          if(false) error=true; // hub.read()!=d
          // Serial.print(" d:");
          Serial.write(hub.read());
        }
        a++;
        if (error) break;
      }
      hub.reset();
    }
  }
  Serial.print(".");
  Serial.println(a);
}

void set_address(uint32_t adr){
  uint32_t _adr;
  _adr = adr;
  for(int i=0; i<LEN_ADDR_PINS; i++){
    digitalWrite(addr_pins[i], _adr & 1);
    _adr = _adr>>1;
  }
  NOP;
}

uint8_t read_byte(uint32_t address){
  uint8_t d=0;
  set_address(address);
  set_data_pins(INPUT);
  
  digitalWrite(OE, LOW);
  delayMicroseconds(2);
  for(int i=7; i>=0; i--){
    d = d + digitalRead(data_pins[i]);
    d = d<<1;
  }
  digitalWrite(OE, HIGH);

  return d;
}

uint8_t write_byte(uint8_t data, uint32_t address){
  uint8_t d;
  d = data;
  set_address(address);
  set_data_pins(OUTPUT);
  for(int i=0; i<8; i++){
    digitalWrite(data_pins[i], d&1);
    d = d>>1;
  }
  digitalWrite(WE, LOW);
  delayMicroseconds(2);
  digitalWrite(WE, HIGH);
  NOP; 
}

void toggle_led(int l){
  digitalWrite(l, !digitalRead(l));
}

uint8_t calculate_crc(uint8_t*buf){
  return '*';
}

void read_rom(uint8_t ch) {
  unsigned long wait_time_start;
  int c=0;
  set_control_pins();
  set_data_pins(INPUT_PULLUP);
  uint16_t a = 0;
  uint8_t retry = 0;
  error = false;
  while(a <= mem_chunks){
    // -------------------------------------------- send a chunk and crc
    for (int i=0; i<block_size; i++){
      buf[i] = read_byte(a*block_size + i);
      Serial.print(a*block_size+i);
      Serial.print(',');
      Serial.print(buf[i]);
      Serial.write(buf[i]);
      Serial.println();
    }
    // Serial.write(buf, block_size);
    // Serial.write(calculate_crc(buf));
    toggle_led(L_READ);
    // ---------------------------------------- handshake to snd next chunk
    wait_time_start = millis();
    while(!Serial.available()){
      if (millis() > wait_time_start + TIMEOUT){
        error=true;
        break;
      }
    }
    c = Serial.read();
    if (c=='+'){
      retry = 0;
      a++;
    }
    if (c=='-'){
      retry++;
      if (retry>20){
        error = true;
        break;
      }
    }
    if(error){
      digitalWrite(L_ERROR, HIGH);
      Serial.write('!');
      print_lcd(0,0, "  *! ERROR !*   ");
      break;
    }
  }
}

void write_rom() {
  set_control_pins();
  set_data_pins(OUTPUT);
  uint16_t a = 0;
  while(a < mem_chunks){
    Serial.readBytes(buf, block_size);
    for (int i=0; i<block_size; i++){
      write_byte(0xAA, 0x55555);
      write_byte(0x55, 0x2AAAA);
      write_byte(0xA0, 0x55555);
      write_byte(buf[i], a*block_size + i);
      delayMicroseconds(10); /* max 300us, typ 7us*/
      }
    a++;
  }
}

void set_addr_pins_output(){
  for (int i = 0; i < LEN_ADDR_PINS; i++) {
    pinMode(addr_pins[i], OUTPUT);
    digitalWrite(addr_pins[i], LOW);
  }
}

void set_data_pins(uint8_t mode){
  for (int i = 0; i < 8; i++) {
    pinMode(data_pins[i], mode);
  }
}

void set_control_pins(){
  digitalWrite(WE, HIGH);
  digitalWrite(OE, HIGH);
  digitalWrite(CE, LOW);
  NOP;
}

void eraseChip(){
  digitalWrite(L_WRITE, HIGH);
  set_control_pins();
  set_data_pins(OUTPUT);

  write_byte(0xAA, 0x55555);
  write_byte(0x55, 0x2AAAA);

  write_byte(0x80, 0x55555);

  write_byte(0xAA, 0x55555);
  write_byte(0x55, 0x2AAAA);

  write_byte(0x10, 0x55555);

  delay(60000); /*8sec typical, 64sec max */
  set_data_pins(INPUT);
  digitalWrite(L_WRITE, LOW);
}
