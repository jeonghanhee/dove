import time

class PacketFactory:
    @staticmethod
    def heartbeat():
        return {
            "type": "heartbeat",
            "timestamp": time.time()
        }

    @staticmethod
    def send_tube(origin: str, destination: str, content: str):
        return {
            "type": "send_tube",
            "origin": origin,
            "destination": destination,
            "content": content,
            "timestamp": time.time()
        }

    # @staticmethod
    # def receive_tube(sender: str, content: str):
    #     return {
    #         "type": "receive_tube",
    #         "sender": sender,
    #         "content": content,
    #         "timestamp": time.time()
    #     }

    # @staticmethod
    # def server_notification(alert: str):
    #     return {
    #         "type": "server_notification",
    #         "alert": alert,
    #         "timestamp": time.time()
    #     }