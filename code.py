#include <Keypad.h>
#include <LiquidCrystal.h>
#include <Servo.h>

Servo myservo;
LiquidCrystal lcd(A0, A1, A2, A3, A4, A5);

// 5 digits for password + 1 for null terminator
#define Password_Length 6

char Data[Password_Length];
char Master[Password_Length] = "24682"; // Your password
byte data_count = 0;
char customKey;

const byte ROWS = 4;
const byte COLS = 3;

// Keypad layout
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

// Same pin mapping from your table
byte rowPins[ROWS] = {2, 3, 4, 5};   
byte colPins[COLS] = {6, 7, 8};

Keypad customKeypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  myservo.attach(9);
  ServoClose();
  lcd.begin(16, 2);
  lcd.print(" Arduino Door");
  lcd.setCursor(0, 1);
  lcd.print("--Lock project--");
  delay(2000);
  lcd.clear();
}

void loop() {
  Open(); // Always wait for password input and handle the process
}

void clearData() {
  while (data_count != 0) {
    Data[--data_count] = 0;
  }
}

void ServoOpen() {
  myservo.write(90); // Open position
}

void ServoClose() {
  myservo.write(0); // Closed position
}

void Open() {
  lcd.setCursor(0, 0);
  lcd.print(" Enter Password   ");

  customKey = customKeypad.getKey();
  if (customKey) {
    // Only accept digits (ignore * and #)
    if (data_count < Password_Length - 1 && customKey != '#' && customKey != '*') {
      Data[data_count] = customKey;
      lcd.setCursor(data_count, 1);
      lcd.print(customKey);  // Show actual number pressed
      data_count++;
    }
  }

  if (data_count == Password_Length - 1) {
    Data[Password_Length - 1] = '\0';

    if (!strcmp(Data, Master)) {
      // Correct password actions
      lcd.clear();
      lcd.print(" Door is Open ");
      ServoOpen();
      delay(5000); // Wait 5 seconds with door open

      ServoClose();
      lcd.clear();
      lcd.print(" Door is Closed ");
      delay(3000); // Wait 3 seconds with door closed

      lcd.clear();
      lcd.print(" Enter Password ");

    } else {
      // Wrong password actions
      lcd.clear();
      lcd.print(" Wrong Password ");
      delay(1500);
      lcd.clear();
      lcd.print(" Enter Password ");
    }

    clearData(); // Reset for next input
  }
}
