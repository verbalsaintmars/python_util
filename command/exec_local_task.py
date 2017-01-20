import subprocess


# Execute local command
def run_command(command, no_wrapper=False, silent=False):
    """exec command
    """
    if no_wrapper:
        proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if stderr:
            log.error("Error running command %s %s", ' '.join(command), stderr)
        return stdout, stderr, proc.returncode
    else:
        (ret, output) = commands.getstatusoutput(command)
        if ret:
            log.error("Executing command %s: %s", command, output)
            if not silent:
                raise ExecErrorException
        return output, None
