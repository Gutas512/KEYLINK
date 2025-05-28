#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <Servo.h>

// Configurações de WiFi
const char* ssid = "Agostinho";
const char* password = "floresta512";

// Configurações do Servo
const int pinoServo = D1;  // GPIO5 (D1 no NodeMCU)
Servo meuServo;

// Servidor Web
ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  
  // Inicializa o servo
  meuServo.attach(pinoServo);
  meuServo.write(0);  // Posição inicial (fechado)
  delay(1000);        // Tempo para o servo se posicionar

  // Conexão WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Rotas do servidor
  server.on("/comando", HTTP_POST, handleComando);
  server.onNotFound(handleNotFound);
  
  server.begin();
  Serial.println("Servidor HTTP pronto");
  Serial.println("Envie comandos POST para /comando");
  Serial.println("Exemplo: {\"comando\":\"Abra\", \"chave_id\":1}");
}

void loop() {
  server.handleClient();
}

// Trata requisições para rotas não encontradas
void handleNotFound() {
  server.send(404, "application/json", "{\"error\":\"Endpoint não encontrado\"}");
}

// Processa comandos do servo
void handleComando() {
  // Verifica se é POST
  if (server.method() != HTTP_POST) {
    server.send(405, "application/json", "{\"error\":\"Método não permitido\"}");
    return;
  }

  // Log da requisição
  String body = server.arg("plain");
  Serial.println("Recebido: " + body);

  // Parse do JSON
  DynamicJsonDocument doc(256);
  DeserializationError error = deserializeJson(doc, body);

  // Verifica erros no JSON
  if (error) {
    String erro = "{\"error\":\"JSON inválido: " + String(error.c_str()) + "\"}";
    server.send(400, "application/json", erro);
    Serial.println(erro);
    return;
  }

  // Verifica campo 'comando'
  if (!doc.containsKey("comando")) {
    server.send(400, "application/json", "{\"error\":\"Campo 'comando' faltando\"}");
    Serial.println("Erro: Campo 'comando' faltando");
    return;
  }

  // Extrai dados do JSON
  String comando = doc["comando"];
  int chave_id = doc.containsKey("chave_id") ? doc["chave_id"] : -1;

  // Executa comandos
  if (comando == "Abra") {
    meuServo.write(180);  // Abre (180°)
    Serial.println("Servo: Aberto (180°) | Chave ID: " + String(chave_id));
    server.send(200, "application/json", "{\"status\":\"Aberto\", \"angulo\":180}");
    
  } else if (comando == "Feche") {
    meuServo.write(0);    // Fecha (0°)
    Serial.println("Servo: Fechado (0°) | Chave ID: " + String(chave_id));
    server.send(200, "application/json", "{\"status\":\"Fechado\", \"angulo\":0}");
    
  } else {
    server.send(400, "application/json", "{\"error\":\"Comando inválido\"}");
    Serial.println("Erro: Comando inválido: " + comando);
  }
}