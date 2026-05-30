import json
from aiortc import RTCPeerConnection, RTCSessionDescription

async def handle_signaling(pc, offer_json):
    # Parse the offer from the AR Wearable
    offer = json.loads(offer_json)
    pc.setRemoteDescription(RTCSessionDescription(
        sdp=offer["sdp"], 
        type=offer["type"]
    ))

    # Generate our answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    # Return the answer to be sent back to the wearable
    return json.dumps({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })
