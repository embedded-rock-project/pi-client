import Motion
import Pulse
import Pressure
from Camera import Camera
class App:
    def __init__(self):
        self.command = input('Rock Proctector Interface> ')
        self.Parse()
        App()
    def Parse(self):
        self.UIshutdwnwords = ('QUIT','EXIT')
        if(self.command.upper() in self.UIshutdwnwords):
            quit()
        self.commandcomp = self.command.split(' ')
        self.Run = self.commandcomp[0]
        for arg in self.commandcomp[2:]:
            print(arg)
        self.Method = self.commandcomp[1]
        self.Args = tuple(self.commandcomp[2:])
        eval(f'{self.Run}().{self.Method}{self.Args}')
if(__name__=='__main__'):
    App()