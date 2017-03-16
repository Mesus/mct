import uuid
mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
real_mac = "".join([mac[e:e+2] for e in range(0,11,2)])
print real_mac
import base64
print base64.b64encode(bytes(real_mac))