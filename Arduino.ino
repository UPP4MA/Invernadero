#include <DHT.h>
#include <DHT_U.h>

const int in1Pin = 11; // Entrada 2 del puente-H
const int in2Pin = 9;  // Entrada 7 del puente-H
int led = 2;
int SENSOR = 5;
int ventilador = 6;
int TIERRA = A0;
int luces = 8;  // Nuevo pin para controlar las luces
int foto = A5;
int var;
int estado_led = LOW;
int estado_ventilador = LOW;
int estado_luces = LOW;
bool secuenciaActivada = false;
int TEMPERATURA;
int umbralLed = 600;  // Valor predeterminado para el umbral del LED
int umbralVentilador = 24;  // Valor predeterminado para el umbral del ventilador

DHT dht(SENSOR, DHT11);

bool girandoMotor = false;
unsigned long tiempoInicio = 0;
const unsigned long tiempoGiro = 3700; // Tiempo de giro

void setup() {
  pinMode(led, OUTPUT);
  pinMode(botonManual, INPUT);
  pinMode(botonSecuencia, INPUT);
  pinMode(ventilador, OUTPUT);
  pinMode(luces, OUTPUT);
  pinMode(var, INPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  Serial.println("Para seleccionar la dirección introduce + o -");
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  while (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "TOGGLE_LED_MANUAL") {
      estado_led = !estado_led;
      digitalWrite(led, estado_led);
    } else if (command == "TOGGLE_SECUENCIA") {
      secuenciaActivada = !secuenciaActivada;
      if (secuenciaActivada) {
        ejecutarSecuencia();
      }
    } else if (command == "TOGGLE_VENTILADOR_MANUAL") {
      estado_ventilador = !estado_ventilador;
      digitalWrite(ventilador, estado_ventilador);
    } else if (command == "TOGGLE_LUCES_MANUAL") {
      estado_luces = !estado_luces;
      digitalWrite(luces, estado_luces);
    } else if (command == "REFRESH_SENSORES") {
      enviarValoresSensores();
    } else if (command == "GIRAR_HORARIO") {
      girarMotorHorario();
    } else if (command == "GIRAR_ANTIHORARIO") {
      girarMotorAntihorario();
    } else if (command.startsWith("U_LED")) {
      int nuevoUmbralLed = command.substring(5).toInt();
      if (nuevoUmbralLed != umbralLed) {
        umbralLed = nuevoUmbralLed;
      }
    } else if (command.startsWith("U_VENT")) {
      int nuevoUmbralVentilador = command.substring(6).toInt();
      if (nuevoUmbralVentilador != umbralVentilador) {
        umbralVentilador = nuevoUmbralVentilador;
      }
    }
  }

  if (secuenciaActivada) {
    ejecutarSecuencia();
  }

  // Verifica si ha pasado el tiempo de giro y detiene el motor
  if (girandoMotor && millis() - tiempoInicio >= tiempoGiro) {
    Serial.println("Deteniendo el motor...");
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
    girandoMotor = false;
  }
}

void ejecutarSecuencia() {
  var = analogRead (foto);
  Serial.println (var);
  TEMPERATURA = dht.readTemperature();
  int humedad = analogRead(TIERRA);

  if (humedad <= umbralLed) {
    digitalWrite(led, LOW);
  } else {
    digitalWrite(led, HIGH);
  }
  if (TEMPERATURA >= umbralVentilador) {
    digitalWrite(ventilador, HIGH);
  } else {
    digitalWrite(ventilador, LOW);
  }
  if (var <= 230){
    digitalWrite (luces, LOW);
   } else if (var >= 230){
    digitalWrite (luces, HIGH);
  }

  Serial.print("H:");
  Serial.print(humedad);
  Serial.print(",");
  Serial.print("T:");
  Serial.println(TEMPERATURA);

  delay(1000);
}

void enviarValoresSensores() {
  int humedad = analogRead(TIERRA);
  TEMPERATURA = dht.readTemperature();

  Serial.print("H:");
  Serial.print(humedad);
  Serial.print(",");
  Serial.print("T:");
  Serial.println(TEMPERATURA);
}

void girarMotorHorario() {
  if (!girandoMotor) {
    Serial.println("Girando en sentido horario...");
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    tiempoInicio = millis();
    girandoMotor = true;
  }
}

void girarMotorAntihorario() {
  if (!girandoMotor) {
    Serial.println("Girando en sentido antihorario...");
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    tiempoInicio = millis();
    girandoMotor = true;
  }
}
