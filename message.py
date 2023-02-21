import functools


class Message:

    def __init__(self, senderId: int = 0,  recieverId: int = 0,  MESSAGE_TYPE: int = 0,  msg=[]):
        self.senderId = senderId
        self.recieverId = recieverId
        self.MESSAGE_TYPE = MESSAGE_TYPE
        if isinstance(msg,  str):
            self.msgStrContent = msg
            self.msgContent = []
        elif isinstance(msg,  list):
            self.msgStrContent = ''
            self.msgContent = msg

    def __str__(self) -> str:
        return f"Message senderId= {self.senderId} recieverId={self.recieverId} MESSAGE_TYPE={self.MESSAGE_TYPE} msgContent={' '.join(map(str, self.msgContent))}"
