# 📱 Combat Bot Pro Controller - Aplicativo Flutter de Baixa Latência

Aplicativo multiplataforma (**Android, iOS, Web e Windows**) desenvolvido em **Flutter / Dart** para controle de alta performance de robôs de combate, otimizando o tempo de resposta e unificando os projetos (**ESP32 V1, ESP32 V2, Arduino + HC-05 e micro:bit**).

---

## ⚡ Por que usar o App Nativo em Flutter em vez do Navegador Web?

| Recurso | Navegador Web do Celular | App Nativo Flutter | Ganho do App Flutter |
| :--- | :--- | :--- | :--- |
| **Taxa de Quadros (FPS)** | ~30 a 60 FPS com instabilidades | **60 a 120 FPS cravados** | Joystick ultra-suave sem micro-travamentos |
| **Latência de Toque (Touch)** | ~30ms a 50ms (overhead do browser) | **< 8ms (Nativo do Sistema Operacional)** | Resposta imediata nos dedos do piloto |
| **Transmissão WebSocket** | JavaScript single-threaded | **Dart Assíncrono com buffer dedicado** | Pacotes a cada 25ms (40 FPS) sem perda |
| **Feedback Háptico (Vibração)** | Inconsistente ou bloqueado | **Vibrações táticas reais (Turbo / Impactos)** | Sentir o choque e a potência no celular |
| **Estabilidade em Segundo Plano** | O Chrome suspende abas ao minimizar | **Conexão persistente com reconexão auto** | Não perde o controle se receber notificação |
| **Modo Offline / Simulação** | Exige Wi-Fi ativo para abrir a página | **Funciona 100% offline (com simulador)** | Treinar e testar manobras em qualquer lugar |

---

## 🎮 Recursos de Combate Implementados no App

1. **🕹️ Joystick Analógico 360° com CustomPainter**:
   - Resposta vetorial polar contínua com cálculo de *Arcade Drive Mixing*.
   - Retorno automático suave ao soltar (*Auto-spring to center*) com frenagem imediata.
   - Zona morta configurável (5% a 20%) para eliminar toques involuntários.
2. **🎛️ Alternador para D-Pad Tático de 8 Direções**:
   - Botões direcionais grandes para quem prefere toques discretos e esquadro perfeito.
3. **🔥 Botão TURBO OVERDRIVE 100%**:
   - Pressionar e segurar aplica PWM máximo (255 no ESP32 ou 1023 no micro:bit) com vibração contínua no celular para momentos de abalroamento e empurrão.
4. **🔄 Manobras Rápidas 90° e 180° com Calibração**:
   - Giros rápidos automáticos com ajuste fino de tempo em milissegundos via menu de configurações.
5. **🎯 Painel de Pivô de Roda Única**:
   - Aciona de forma isolada a roda esquerda ou direita (frente e ré) com a outra roda travada como âncora fixa.
6. **⚔️ Controle de Arma / Atuador**:
   - Botão de acionamento com indicador de estado (Armada / Desarmada).
7. **🛑 Parada de Emergência (E-Stop)**:
   - Botão de corte imediato que desliga todos os motores instantaneamente.
8. **📊 Telemetria e Monitor de Ping**:
   - Exibição da potência real aplicada em cada motor (L e R) com sentido de rotação.
   - Monitor de ping / latência em milissegundos em tempo real.

---

## 🚀 Como Rodar e Instalar no Celular

### Opção 1: Gerar o APK para instalar no Android (Recomendado)
No terminal, dentro da pasta `flutter_controller/`:
```bash
flutter build apk --release
```
O arquivo gerado estará em:
`build/app/outputs/flutter-apk/app-release.apk`
Basta transferir esse arquivo para o seu celular Android (via WhatsApp, Google Drive ou cabo USB) e instalar diretamente!

---

### Opção 2: Testar no Celular via Cabo USB (Modo Desenvolvedor)
1. Conecte o celular no computador via cabo USB com a **Depuração USB** ativada.
2. No terminal:
```bash
cd flutter_controller
flutter run
```

---

### Opção 3: Rodar no Navegador Web (Chrome)
Para testar na tela do computador sem precisar de celular:
```bash
cd flutter_controller
flutter run -d chrome
```

---

## ⚙️ Configurações Rápidas (Ícone da Engrenagem)

No canto superior direito do app, toque no ícone de engrenagem para ajustar:
* **Protocolo de Conexão**:
  - `⚡ WebSockets`: Para o firmware **ESP32 V2** (ultra-baixa latência < 5ms).
  - `🌐 HTTP REST`: Para o firmware **ESP32 V1** ou redes Wi-Fi restritas.
  - `🎮 Simulação Local`: Para testar a interface e o joystick sem robô físico.
* **IP do Robô**: Padrão `192.168.4.1`.
* **Tempo do Giro de 90°**: Calibre de 150ms a 500ms de acordo com o atrito da arena.
* **Potência Máxima Padrão**: 50% a 100%.
* **Zona Morta do Analógico**: 5% a 20%.
