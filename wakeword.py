import speech_recognition as sr
import websockets
import asyncio
import threading

connected_clients = set()

async def websocket_server(websocket):
    connected_clients.add(websocket)
    print(f"✅ Client connected")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

def broadcast_detection():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for ws in list(connected_clients):
        try:
            loop.run_until_complete(ws.send("detect"))
        except:
            connected_clients.remove(ws)

def listen_for_wake_word():
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    # All possible variations of "Moses"
    moses_variations = [
        'moses',
        'mozes',
        'mosis',
        'mosus',
        'moises',
        'moyses',
        'moshe',
        'mo ses',
        'mo sis',
        'mose',
        'mozis',
        'mouses',
        'mousses'
    ]
    
    print("🎤 Listening for 'Moses' (all variations)...")
    
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
    
    while True:
        try:
            with mic as source:
                # Lower pause threshold to catch quick speech
                r.pause_threshold = 0.8
                audio = r.listen(source, timeout=None, phrase_time_limit=5)
            
            try:
                text = r.recognize_google(audio).lower()
                print(f"📝 Heard: {text}")
                
                # Check if ANY variation of Moses is in the text
                if any(variation in text for variation in moses_variations):
                    print("🔥 MOSES DETECTED!")
                    broadcast_detection()
                    
            except sr.UnknownValueError:
                # Couldn't understand audio - just continue
                pass
            except sr.RequestError as e:
                print(f"❌ Recognition error: {e}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

async def main():
    server = await websockets.serve(websocket_server, "localhost", 10401)
    print("🌐 WebSocket server started on ws://localhost:10401")
    threading.Thread(target=listen_for_wake_word, daemon=True).start()
    await asyncio.Future()

asyncio.run(main())
