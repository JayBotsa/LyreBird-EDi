import time, threading, base64, hashlib

# Instance: the humming device (e.g., borehole pump)
class Instance:
    def __init__(self, id="0065050298000000000001760676115237ZZ"):
        self.id = id
        self.owner_key = hashlib.sha256(b"ALPHAOMEGA").hexdigest()  # Owner's half
        self.data = "Gene060AN2153,45,2.3,37.8,-122.4,SW"  # Real packet
        self.handshake = "ALPHAOMEGA::agriculture-update::handshake-ok"

    def flash(self, hook_id, protocol):
        # Flash: instance ID + timestamp + data + handshake
        timestamp = int(time.time())
        full_packet = f"{self.id}::{timestamp}::{self.data}::{self.handshake}"
        if hook_id == self.owner_key:
            return full_packet  # Owner sees everything
        # Protocol filters: each hook gets only its pixel
        values = self.data.split(",")
        if protocol == "soil-depth-protocol":
            return f"{self.handshake}::depth={values[0][10:]}mm"  # 2153
        elif protocol == "route-calc-protocol":
            return f"{self.handshake}::speed={values[2]}m/s,gps={values[3]},{values[4]}"  # 2.3,37.8,-122.4
        elif protocol == "threshold-rise-protocol":
            return f"{self.handshake}::alert={int(values[1]) < 30}"  # 45 < 30? False
        return base64.b64encode(full_packet.encode()).decode()  # Static to outsiders

# Simulate chirpnet: multiple hooks listening
def chirpnet_sim():
    pump = Instance()
    hooks = [
        ("weather_hook", "soil-depth-protocol"),
        ("supply_hook", "route-calc-protocol"),
        ("alert_hook", "threshold-rise-protocol"),
        ("outsider", "none")
    ]
    for hook_id, protocol in hooks:
        result = pump.flash(hook_id, protocol)
        print(f"{hook_id} sees: {result}")

# Run eternal hum
threading.Thread(target=chirpnet_sim, daemon=True).start()
time.sleep(1)  # Let it flash once
