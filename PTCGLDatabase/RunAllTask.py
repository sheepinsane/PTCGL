import subprocess
import sys

def run_batch_commands(num_batches, batch_size):
    for batch in range(num_batches):
        start = batch * batch_size + 1
        end = (batch + 1) * batch_size
        command = ['python', 'GetCardInfo.py', str(start), str(end)]
        subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    num_batches = 15
    batch_size = 1000
    run_batch_commands(num_batches, batch_size)