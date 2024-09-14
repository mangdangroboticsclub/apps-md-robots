import subprocess
import logging

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(e.stderr)


import argparse
import sys
def main(args):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO
    )

    if args.cmd:
        execute_command(args.cmd)
        sys.exit()

    while True:
        user_input = input("input shell command or 'exit': ").strip().lower()

        if user_input == 'exit':
            logging.info("Exit!")
            break
        else:
            execute_command(user_input)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute shell commands.')
    parser.add_argument('--cmd', type=str, help='Execute the provided shell command without interactive prompt.')

    args = parser.parse_args()

    main(args)

