# Moses AI - Voice-Controlled Smart Home Assistant

A complete voice-controlled smart home system using Home Assistant, Broadlink RM4 Pro, and n8n for AI automation.

## Features

- 🎤 Wake word detection ("Moses" or "Jarvis")
- 🗣️ Natural voice commands with AI processing
- 🌡️ Control IR/RF devices (AC, TV, fans, etc.) via Broadlink RM4 Pro
- 📊 Beautiful dashboard with weather, calendar, and sun position
- 🔊 Text-to-speech responses
- ✨ Animated voice visualization

## System Requirements

- Windows 10/11 (or adapt for Linux/Mac)
- Python 3.8+
- Docker Desktop
- Microphone
- Broadlink RM4 Pro on same network
- OpenAI API key (for n8n AI agent)

## Installation

### 1. Install Python Dependencies
```bash
pip install speechrecognition==3.10.0 websockets==12.0 pyaudio==0.2.14 pvporcupine==3.0.2
```

### 2. Install Docker Containers

**Home Assistant:**
```bash
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Singapore \
  -v homeassistant_config:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

**n8n:**
```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e GENERIC_TIMEZONE="Asia/Singapore" \
  -e TZ="Asia/Singapore" \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### 3. Configure Home Assistant

1. Open Home Assistant: `http://localhost:8123`
2. Complete initial setup
3. Go to **Settings → Devices & Services**
4. Click **Add Integration** → Search "Broadlink"
5. Follow prompts to add your RM4 Pro
6. Learn IR/RF codes:
   - Go to **Developer Tools → Actions**
   - Action: `remote.learn_command`
   - Target: Your Broadlink entity
   - Device: `aircon` (or your device name)
   - Command: `power on` (or button name)
   - Command type: `ir` or `rf`
   - Click "Perform action"
   - Point your remote at RM4 and press button

### 4. Import n8n Workflows

1. Open n8n: `http://localhost:5678`
2. Import these workflows:
   - `n8nAirconBot.json` - Main AI agent
   - `n8n-htmldashboard.json` - Dashboard status endpoint
   - `n8n-trigger.json` - Wake word trigger
3. In the Aircon Bot workflow:
   - Add your OpenAI API key to the OpenAI Chat Model node
   - Update the Home Assistant URL and entity IDs in HTTP Request nodes
4. Activate all workflows

### 5. Configure Wake Word Detection

Choose ONE method:

**Option A: Google Speech Recognition (wakeword.py)**
- No API key needed
- Uses Google's speech recognition
- Detects "Moses" and variations
- Less accurate but free

**Option B: Porcupine (bridge.py)**
- Requires Porcupine account (free tier available)
- More accurate wake word detection
- Detects "Jarvis"
- Get API key from [Picovoice Console](https://console.picovoice.ai/)

## Usage

### Start the System

1. **Start Docker containers:**
```bash
   docker start homeassistant n8n
```

2. **Run wake word detection:**
```bash
   # For Google Speech Recognition
   python wakeword.py
   
   # OR for Porcupine
   python bridge.py
```

3. **Open dashboard:**
   - Double-click `Moses.html` or
   - Open in browser: `file:///path/to/Moses.html`

4. **Click "Enable Voice Assistant"** when page loads

5. **Say the wake word:**
   - "Moses" (if using wakeword.py)
   - "Jarvis" (if using bridge.py)

6. **Give your command:**
   - "Turn on the air conditioner"
   - "Make it cooler"
   - "Set fan to high"
   - "What's 25 times 4?"

### Example Commands

- "Turn on my air con"
- "Turn off the AC"
- "Increase the temperature"
- "Decrease the temperature"
- "Set fan to speed 1/2/3/4"
- "What's [math problem]?"

## Troubleshooting

### Wake Word Not Detecting

- Check microphone permissions
- Ensure Python script is running
- Look for "🎤 Listening for..." message
- Try speaking louder/clearer

### Voice Commands Not Working

- Check n8n workflows are active
- Verify Home Assistant is running
- Check browser console (F12) for errors
- Ensure WebSocket connection shows "✅ Wake word connected"

### Broadlink Not Responding

- Verify RM4 Pro is powered on
- Check it's on same network
- Test commands in Home Assistant first
- Re-learn codes if necessary

### No Speech Output

- Click "Enable Voice Assistant" button first
- Check browser allows audio autoplay
- Try different browser (Chrome works best)

## Project Structure
```
├── Moses.html              # Main dashboard
├── wakeword.py            # Google Speech Recognition wake word
├── bridge.py              # Porcupine wake word detection
├── n8nAirconBot.json      # AI agent workflow
├── n8n-htmldashboard.json # Dashboard status endpoint
├── n8n-trigger.json       # Wake word webhook
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Customization

### Add More Devices

1. Learn new IR/RF codes in Home Assistant
2. Add new HTTP Request Tool nodes in n8n Aircon Bot workflow
3. Update the system message to include new commands

### Change Wake Word

**For wakeword.py:** Edit the `moses_variations` list

**For bridge.py:** Change `keywords=['jarvis']` to another Porcupine keyword

### Customize Dashboard

Edit `Moses.html` to:
- Change colors (search for `#78c8ff`)
- Modify location (weather API coordinates)
- Add/remove dashboard widgets

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License - feel free to use and modify!

## Credits

- Home Assistant for smart home platform
- n8n for workflow automation
- Broadlink for IR/RF hardware
- Picovoice for Porcupine wake word engine
