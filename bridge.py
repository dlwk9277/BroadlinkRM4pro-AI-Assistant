import pvporcupine
import pyaudio
import struct
import websockets
import asyncio

connected_clients = set()

async def websocket_server(websocket):
    connected_clients.add(websocket)
    print(f"✅ Client connected")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def broadcast_detection():
    for ws in list(connected_clients):
        try:
            await ws.send("detect")
        except:
            connected_clients.remove(ws)

def listen_for_wake_word():
    porcupine = pvporcupine.create(keywords=['jarvis'])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    print("🎤 Listening for 'Jarvis'...")
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        if porcupine.process(pcm) >= 0:
            print("🔥 JARVIS DETECTED!")
            asyncio.run(broadcast_detection())

async def main():
    server = await websockets.serve(websocket_server, "localhost", 10401)
    await asyncio.get_event_loop().run_in_executor(None, listen_for_wake_word)

asyncio.run(main())
