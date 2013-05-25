#!/usr/bin/python


import sys
import time
import shlex
import subprocess
from daemon import runner

class Misc():
    @staticmethod
    def read_file(filename):
        file_object = open(filename)
        file_dat    = file_object.read()
        file_object.close()
        return file_dat.strip()

    @staticmethod
    def run_in_terminal(command):
        handle = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        if handle:
            return handle
        else:
            return None

    @staticmethod
    def terminate(pid):
        command = 'sudo kill -1 %d' %(int(pid))
        run_in_terminal(command)
        





class Battery_Manager(Misc):
    def __init__(self):
        self.handle     = ''
        self.alert_stat = False
        self.MEDIA_ROOT = '/home/elimence/batmon/sounds'
        self.SYS_ROOT   = '/sys/class/power_supply'

        self.audio      = {'RedAlert': '%s/redalert.mp3' %(self.MEDIA_ROOT),
                            'Missile': '%s/missile.mp3'  %(self.MEDIA_ROOT)}

        self.stat_loc   = {'BATTERY_CHARGING': '%s/AC/online'   %(self.SYS_ROOT),
                            'BATTERY_LEVEL': '%s/BAT0/capacity' %(self.SYS_ROOT)}

    
    def check_ac (self):
        # add code to check if battery is charging
        charging_status = Misc.read_file(self.stat_loc['BATTERY_CHARGING'])

        if charging_status == '1':
            return True
        else:
            return False


    def check_level (self):
        # add code to check battery level
        battery_level = Misc.read_file(self.stat_loc['BATTERY_LEVEL'])
        return battery_level

    
    def start_alert (self):
        # add code to sound an alarm
        if not self.alert_stat:
            command = 'cvlc --loop %s' % self.audio['RedAlert']
            self.handle = Misc.run_in_terminal(command)
            self.alert_stat = True

    
    def stop_alert(self):
        if self.alert_stat:
            self.handle.kill()
            self.alert_stat = False
        



class Daemon_Mode():
    def __init__(self):
        self.stdin_path      = '/dev/null'
        self.stdout_path     = '/dev/tty'
        self.stderr_path     = '/dev/tty'
        self.pidfile_path    =  '/home/elimence/batmon/gen/dae.pid'
        self.pidfile_timeout = 5

        self.battery_man = Battery_Manager()


    def run(self):
        while True:
            status = self.battery_man.check_ac()
            if not status:
                self.battery_man.start_alert()
            else:
                self.battery_man.stop_alert()
            time.sleep(2)



app = Daemon_Mode()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()