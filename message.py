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

    # def __eq__(self, other):
    #     if not isinstance(other, Message):
    #         return False
    #     if self.senderId != other.senderId:
    #         return False
    #     if self.recieverId != other.recieverId:
    #         return False
    #     if self.MESSAGE_TYPE != other.MESSAGE_TYPE:
    #         return False
    #     if self.msgStrContent != other.msgStrContent:
    #         return False
    #     if not functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, self.msgContent, other.msgContent), True):
    #         return False
    #     return True

    def __str__(self) -> str:
        return f"Message senderId= {self.senderId} recieverId={self.recieverId} MESSAGE_TYPE={self.MESSAGE_TYPE} msgContent={' '.join(map(str, self.msgContent))}"
