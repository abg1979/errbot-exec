# -*- coding: utf-8 -*-
import os, re, subprocess
from errbot import BotPlugin, botcmd, re_botcmd, ValidationException
from subprocess import Popen
import logging

class Exec(BotPlugin):
    """
    Execute a command when the bot is talked to
    """

    @botcmd(split_args_with=' ', template="output")
    def run_exec(self, msg, args):
        """
        Execute the commmand
        """
        ret_code, stdout, stderr = self.run_cmd(args)
        return {'stdout': stdout, 'stderr': stderr, 'return_code': ret_code}

    def run_cmd(self, args, log_level='DEBUG'):
        process = Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err_output = process.communicate()
        retcode = process.poll()

        if output is not None:
            for subprocess_output_line in output.splitlines():
                self.log.log(logging.getLevelName(log_level), 'STDOUT: %s' % subprocess_output_line)
        if err_output is not None:
            for subprocess_error_line in err_output.splitlines():
                self.log.log(logging.getLevelName(log_level), 'STDERR: %s' % subprocess_error_line)
        return retcode, output, err_output


class ProcessExecutionException(Exception):
    """This exception is raised when a process run by check_call() or
    check_output() returns a non-zero exit status.
    The exit status will be stored in the returncode attribute;
    check_output() will also store the output in the output attribute.
    """

    def __init__(self, exception=None, returncode=0, cmd=None, output=None, *args, **kwargs):
        super(ProcessExecutionException, self).__init__(*args, **kwargs)
        if exception is not None:
            if hasattr(exception, 'returncode'):
                self.returncode = exception.returncode
            if hasattr(exception, 'cmd'):
                self.cmd = exception.cmd
            if hasattr(exception, 'output'):
                self.output = exception.output
        else:
            self.returncode = returncode
            self.cmd = cmd
            self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)



