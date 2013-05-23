class Alert(Misc):
    def __init__(self):
        self.stdin_path      = '/dev/null'
        self.stdout_path     = '/dev/tty'
        self.stderr_path     = '/dev/tty'
        self.pidfile_path    =  '/home/elimence/batmon/gen/alert.pid'
        self.pidfile_timeout = 5

    def run(self):
        command = 'cvlc --loop %s' % self.audio['RedAlert']
        Misc.run_in_terminal(command)