from time import sleep
from message import Message
from threading import Thread, Condition

class MailManager(Thread):

    def __init__(self, MAX_NODE, MAX_MSG=0,  ):
        self.MAX_MSG = MAX_MSG
        self.current_iter = 0
        self.isCurrentIterDone = [False] * (MAX_NODE)
        self.messages = []
        self.costMessages = []
        self.bestMessages = []
        self.lock = Condition()
        super().__init__()

    def run(self):
        try:
            while True:
                # producing a message to send to the consumer
                # putMessage();
                # producer goes to sleep when the queue is full
                # java.lang.Thread.sleep(1000)
                sleep(1)
        except Exception as e:
            pass
    # synchronized(OperateEndCount){
    # while(OperateEndCount.intValue()<this.totalAgentCount.intValue())
    # try {
    # OperateEndCount.wait();
    # } catch (InterruptedException e) {
    # // TODO Auto-generated catch block
    # e.printStackTrace();
    # }
    # }

    def makeTrue(self, node):
        self.lock.acquire()
        if node < len(self.isCurrentIterDone): 
            self.isCurrentIterDone[node] = True
        self.lock.release()

    def makeFalse(self, node):
        self.lock.acquire()
        if node < len(self.isCurrentIterDone):
            self.isCurrentIterDone[node] = False
        self.lock.release()

    def checkAllTrue(self, callingNode):
        self.lock.acquire()
        if not self.isAllTrue(self.isCurrentIterDone):
            self.lock.wait()
        self.lock.notify_all()
        self.lock.release()

    def isAllTrue(self, array):
        self.lock.acquire()
        for b in self.isCurrentIterDone:
            if (not b):
                self.lock.release()
                return False
        self.lock.release()
        return True
        

    def isAllFalse(self, array):
        self.lock.acquire()
        for b in self.isCurrentIterDone:
            if (b):
                self.lock.release()
                return False
        self.lock.release()
        return True

    def startNewIter(self):
        # if(!isAllTrue(isCurrentIterDone) && !isAllFalse(isCurrentIterDone))
        # {
        # wait();
        #
        # }
        # Arrays.fill(self.isCurrentIterDone,False)
        self.lock.acquire()
        self.isCurrentIterDone = [False] * len(self.isCurrentIterDone)
        self.lock.release()

    def putMessage(self, msg):
        self.lock.acquire()
        # checks whether the queue is full or not
        while len(self.messages) == self.MAX_MSG:
            # System.out.println("Waiting on putmsg "+ msg.getSenderId() + " = "+
            # messages.size()+" " + MAX_MSG);
            # waits for the queue to get empty
            self.lock.wait()
        # then again adds element or messages
        self.messages.append(msg)
        # System.out.println(messages);
        self.lock.notify_all()
        self.lock.release()

    def getMessage(self):
        self.lock.acquire()
        while len(self.messages) == 0:
            # System.out.println("Waiting on rcvmsg");
            self.lock.wait()
        # System.out.println("getmsg " + messages.toString());
        message = self.messages[0]
        # extracts the message from the queue
        # self.messages.remove(message)
        del self.messages[0]
        # System.out.println("after getmsg " + messages.toString());
        self.lock.notify_all()
        self.lock.release()
        return message

    def putCostMessage(self, msg):
        self.lock.acquire()
        # checks whether the queue is full or not
        while len(self.costMessages) == self.MAX_MSG:
            # System.out.println("Waiting on cost putmsg "+ msg.getSenderId() + " = "+
            # costMessages.size()+" " + MAX_MSG);
            # waits for the queue to get empty
            self.lock.wait()
        # then again adds element or messages
        self.costMessages.append(msg)
        # System.out.println(messages);
        self.lock.notify_all()
        self.lock.release()

    def getCostMessage(self):
        self.lock.acquire()
        while len(self.costMessages) == 0:
            # System.out.println("Waiting on cost rcvmsg");
            self.lock.wait()
        # System.out.println("get costmsg " + costMessages.toString());
        costmessage = self.costMessages[0]
        # extracts the message from the queue
        # self.costMessages.remove(costmessage)
        del self.costMessages[0]
        # System.out.println("after getmsg " + costMessages.toString());
        self.lock.notify_all()
        self.lock.release()
        return costmessage

    def putBestMessage(self, msg):
        self.lock.acquire()
        # checks whether the queue is full or not
        while len(self.bestMessages) == self.MAX_MSG:
            # System.out.println("Waiting on best putmsg "+ msg.getSenderId() + " = "+
            # bestMessages.size()+" " + MAX_MSG);
            # waits for the queue to get empty
            self.lock.wait()
        # then again adds element or messages
        self.bestMessages.append(msg)
        self.lock.notify_all()
        self.lock.release()

    def getBestMessage(self):
        self.lock.acquire()
        while len(self.bestMessages) == 0:
            self.lock.wait()
        bestmessage = self.bestMessages[0]
        # extracts the message from the queue
        del self.bestMessages[0]
        # self.bestMessages.remove(bestmessage)
        self.lock.notify_all()
        self.lock.release()
        return bestmessage
