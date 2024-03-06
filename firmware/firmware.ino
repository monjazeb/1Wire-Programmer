#include <OneWire.h>
#include <LiquidCrystal.h>
#include <FastLED.h>

//------------------------------------ Hardware Setup
#define LED_PIN 13
#define COLOR_ORDER GRB
#define CHIPSET WS2811
#define NUM_LEDS 1
#define BRIGHTNESS  200

#define SW1 2
#define SW2 53

#define WIRE1 18
#define WIRE2 17

#define L_READ 5
#define L_WRITE 4
#define L_ERROR 3

#define D4 10
#define D5 9
#define D6 8
#define D7 7
#define EN 11
#define RS 12

#define WE 23
#define OE 37
#define CE 41

#define LEN_ADDR_PINS 19
const uint8_t addr_pins[] = {44, 42, 40, 38, 36, 34, 32, 30, 31, 33, 39, 35, 28, 29, 27, 26, 24, 25, 22};
const uint8_t data_pins[] = {46, 48, 50, 51, 49, 47, 45, 43};
//---------------------------------------------------

#define block_size 32
uint16_t mem_chunks = 256;
String command;
char error = 0;
uint8_t bus = 0;
uint8_t chip = 0;
uint8_t buf[block_size+3];
uint8_t addr[8];
String buses[2] = {"EEPROM", "1Wire "};
//----------------------------------- Initiate things
OneWire hub1(WIRE1);
OneWire hub2(WIRE2);
OneWire* hub;
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);
CRGB leds[NUM_LEDS];

void setup() {
  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);

  pinMode(L_READ, OUTPUT);
  pinMode(L_WRITE, OUTPUT);
  pinMode(L_ERROR, OUTPUT);

  pinMode(WE, OUTPUT);
  pinMode(OE, OUTPUT);
  pinMode(CE, OUTPUT);
  digitalWrite(WE, HIGH);
  digitalWrite(OE, HIGH);
  digitalWrite(CE, HIGH);

  set_addr_pins_output();
  set_data_pins(INPUT);

  digitalWrite(L_ERROR, HIGH);
  delay(200);
  digitalWrite(L_WRITE, HIGH);
  delay(200);
  digitalWrite(L_READ, HIGH);
  delay(200);
  digitalWrite(L_ERROR, LOW);
  digitalWrite(L_READ, LOW);
  digitalWrite(L_WRITE, LOW);

  Serial.setTimeout(500);
  Serial.begin (115200);
  lcd.begin(16, 2);
  print_lcd(0, 0, "*ARM Programmer*");
  print_lcd(0, 1, "Connecting...   ");
  digitalWrite(L_ERROR, HIGH);
  while (true) {
    while (!Serial.available());
    if (Serial.read() == 'C') {
      digitalWrite(L_ERROR, LOW);
      print_lcd(0, 0, "Chip:      ");
      print_lcd(10, 0, buses[0]);
      print_lcd(0, 1, "Connected.      ");
      Serial.print('>');
      break;
    }
  }
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness( BRIGHTNESS );
  leds[0] = CRGB::White;
  FastLED.show();
}

//----------------------------------------- Main Loop
void loop() {
  if (Serial.available()) {
    command = Serial.readString();
    run_command(command);
  }
  if (digitalRead(SW1) == LOW) {
    //    read_chip();
    digitalWrite(L_READ, HIGH);
    delay(1000);
    digitalWrite(L_READ, LOW);
  }
  if (digitalRead(SW2) == LOW) {
    //    write_chip();
    digitalWrite(L_WRITE, HIGH);
    delay(1000);
    digitalWrite(L_WRITE, LOW);
  }
}

void print_lcd(uint8_t x, uint8_t y, String text) {
  lcd.setCursor(x, y);
  lcd.print(text);
}

void run_command(String command) {
  switch (command[0]) {
    case 'C': {
        Serial.flush();
        Serial.print(">");
        break;
      }
    case 'S': {
        if (command[1] == 'R') {
          bus = 0;
        }
        if (command[1] == '1') {
          bus = 1;
        }
        print_lcd(10, 0, buses[bus]);
        Serial.print(":");
        Serial.println(bus,HEX);
        break;
      }
    case 'R': {
        print_lcd(0, 1, "Reading...      ");
        digitalWrite(L_READ, HIGH);
        switch (command[1]) {
          case 'R': {
              read_rom(mem_chunks);
              break;
            }
          case '1': {
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
        switch (command[1]) {
          case 'R': {
              write_rom();
              break;
            }
          case '1': {
              write_1wire();
              break;
            }
        }
        digitalWrite(L_WRITE, LOW);
        print_lcd(10, 1, ".Done.");
        break;
      }
    case 'M': {
      mem_chunks = command.substring(1).toInt();
      print_lcd(0, 1, "Size: ");
      print_lcd(0, 7, String(mem_chunks*block_size, 16));
      Serial.println(mem_chunks, HEX);
    }
  }
}

bool find_1wire() {
  byte leemem[3] = {0xF0 , 0x00 , 0x00};
  byte ccrc;
  byte ccrc_calc;

  if (hub1.reset()) hub = &hub1;
  else if (hub2.reset()) hub = &hub2;
  else {
    hub = 0;
    print_lcd(6, 0, "Not found!");
    Serial.print("x");
    return false;
  }
  hub->reset_search();
  if(!hub->search(addr)){
    hub = 0;
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
  while (!find_1wire()) delay(3000);
  uint16_t chunks;
  if (hub) {
    if (chip) {
      chunks = ch;
      hub->write(0xF0 , 1);
      hub->write(0x00 , 1);
      hub->write(0x00 , 1);
      while (chunks) {
        hub->read_bytes(buf, block_size);
        Serial.write(buf, block_size);
        chunks--;
        if (error) break;
      }
    }
  }
  Serial.print('.');
}

void write_1wire() {
  while (!find_1wire()) delay(3000);
  uint16_t chunks = 0;
  if (hub) {
    if (chip) {
      while (Serial.available() <=0);
      hub->write(0x0F , 1);
      hub->write(0x00 , 1);
      hub->write(0x00 , 1);
      while (Serial.available() > 0) {
        Serial.readBytes(buf, block_size);
        hub->write_bytes(buf, block_size, 1);
        chunks++;
        if (error) break;
      }
    }
  }
  Serial.print(".");
  Serial.println(chunks);
}

void set_address(uint32_t adr){
  uint32_t _adr;
  _adr = adr;
  for(int i=0; i<LEN_ADDR_PINS; i++){
    digitalWrite(addr_pins, _adr & 1);
    _adr = _adr>>1;
  }
}

uint8_t read_byte(uint32_t address){
  uint8_t d=0;
  set_address(address);
  
  digitalWrite(OE, LOW);
  delayMicroseconds(1);
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

  for(int i=0; i<8; i++){
    digitalWrite(data_pins[i], d&1);
    d = d>>1;
  }
  digitalWrite(WE, LOW);
  delayMicroseconds(1);
  digitalWrite(WE, HIGH); 
}

void read_rom(uint8_t ch) {
  set_control_pins();
  set_data_pins(INPUT);
  uint16_t a = 0;
  while(a < mem_chunks){
    for (int i=0; i<block_size; i++){
      buf[i] = read_byte(a*i);
      }
    a++;
    Serial.write(buf, block_size);
  }
}

void write_rom() {
  set_control_pins();
  set_data_pins(OUTPUT);
  uint16_t a = 0;
  while(a < mem_chunks){
    Serial.readBytes(buf, block_size);
    for (int i=0; i<block_size; i++){
      write_byte(0xAA, 0x5555);
      write_byte(0x55, 0x2AAA);
      write_byte(0xA0, 0x5555);
      write_byte(buf[i], a*block_size + i);
      delayMicroseconds(30);
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
}

void eraseChip(){
  set_control_pins();
  set_data_pins(OUTPUT);

  write_byte(0xAA, 0x5555);
  write_byte(0x55, 0x2AAA);
  write_byte(0x80, 0x5555);
  write_byte(0xAA, 0x5555);
  write_byte(0x55, 0x2AAA);
  write_byte(0x10, 0x5555);

  delay(100);
  set_data_pins(INPUT);
}
