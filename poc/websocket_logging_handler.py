import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class WebSocketLoggingHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "log_group",
            {
                "type": "log.message",
                "message": log_entry,
            }
        )
        print(f"Log message sent to group: {log_entry}")
