from microWebSrv import MicroWebSrv
import kettle, kettleConfig, gc, json, time, os, hashlib, binascii, uasyncio

clients = set()

last_status = ''

class KettleClient:
    def __init__(self, socket):
        socket.kettle_client = self
        self.socket = socket
        self.last_ticks_ms = time.ticks_ms()
        self.challenge_string = binascii.hexlify(os.urandom(32)).decode('ascii')
        self.authenticated = False
    
    def authenticate(self, challenge_response):
        sha = hashlib.sha256(kettleConfig.KETTLE_PASSWORD)
        sha.update(self.challenge_string)
        if challenge_response == binascii.hexlify(sha.digest()).decode('ascii'):
            self.challenge_string = None
            self.authenticated = True
            self.touch()
            return True
        
        return False
    
    def touch(self):
        self.last_ticks_ms = time.ticks_ms()
        
    def ticksMsFromLastTouch(self):
        return time.ticks_diff(time.ticks_ms(), self.last_ticks_ms)

def init():
    srv = MicroWebSrv(webPath='/web/')
    srv.AcceptWebSocketCallback = _acceptWebSocketCallback
    srv.Start(threaded=True)
    
    uasyncio.create_task(_statusTimerCallback())
    uasyncio.create_task(_deadClientsTimerCallback())
    uasyncio.get_event_loop().run_forever()
    
def _acceptWebSocketCallback(webSocket, httpClient):
    webSocket.RecvTextCallback   = _recvUnauthTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback     = _closedCallback
    
    new_client = KettleClient(webSocket)
    
    clients.add(new_client)
    webSocket.SendText(f'{{"t":"challenge","d":"{new_client.challenge_string}"}}')

def _recvUnauthTextCallback(webSocket, msg):
    try:
        message = json.loads(msg)
    except Exception as ex:
        print(f'failed to parse {msg}: {ex}')
        webSocket.Close()
        return
    
    kettle_client = webSocket.kettle_client
    
    print(message)
    
    response = {'t':'response'}
    
    try:
        response['i'] = int(message['i'])
        
        if message['o'] != 'challenge':
            webSocket.Close()
        elif kettle_client.authenticate(message['d']):
            print('challenge success')
            webSocket.RecvTextCallback   = _recvAuthTextCallback
            response['d'] = True
            webSocket.SendText(json.dumps(response))
            webSocket.SendText(f'{{"t":"status","d":{kettle.leds_json()}}}')
        else:
            print('challenge fail')
            response['d'] = False
            webSocket.SendText(json.dumps(response))
            webSocket.Close()
            
    except Exception as ex:
        print(f'auth failed {msg}: {ex}')
        webSocket.Close()
    finally:
        gc.collect()

def _recvAuthTextCallback(webSocket, msg):
    try:
        message = json.loads(msg)
    except Exception as ex:
        print(f'failed to parse {msg}: {ex}')
        webSocket.Close()
        return
    
    kettle_client = webSocket.kettle_client
    kettle_client.touch()
    
    print(message)
    
    response = {'t':'response'}
        
    try:
        response['i'] = int(message['i'])
        
        if message['o'] == 'ping':
            response['d'] = 'pong'
        elif message['o'] == 'button_press':
            kettle.press_button(message['d'])
    except Exception as ex:
        response['e'] = str(ex)
    else:
        if not 'd' in response:
            response['d'] = 'ok'
    finally:
        print(f'response: {response}')
        webSocket.SendText(json.dumps(response))
        gc.collect()

def _recvBinaryCallback(webSocket, data):
    webSocket.Close()

def _closedCallback(webSocket):
    clients.remove(webSocket.kettle_client)
  
async def _statusTimerCallback():
    while True:
        await uasyncio.sleep_ms(100)
        
        #print('statustimer')
        
        try:
            if sum(1 for _ in filter(lambda x: x.authenticated, clients)) == 0:
                continue
                
            status = kettle.leds_json()
            
            global last_status
            
            if status == last_status:
                continue
            
            last_status = status
            status_msg = f'{{"t":"status","d":{status}}}'
            
            #print(f'sending {status_msg} to all clients')
            
            for client in clients:
                if client.authenticated:
                    client.socket.SendText(status_msg)
                
            gc.collect()
        except Exception as ex:
            print(ex)
    
async def _deadClientsTimerCallback():
    while True:
        await uasyncio.sleep_ms(5000)
        
        #print('deadclientstimer')
        
        try:
            for client in clients:
                if client.ticksMsFromLastTouch() > \
                   (kettleConfig.KEEPALIVE_AUTH_MS if client.authenticated else kettleConfig.KEEPALIVE_UNAUTH_MS):
                    print(f'dead client: {client.authenticated} {client.challenge_string}')
                    client.socket.Close()
        except Exception as ex:
            print(ex)
        
