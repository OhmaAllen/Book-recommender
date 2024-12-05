from UserInterface import UserInterface
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', help='force load of the application')
    parser.add_argument('-t', '--test', action='store_true', help='run in test mode')
    parser.add_argument('-l', '--login', type=str, default=None, help='user to login as')
    return parser.parse_args()


def main():
    args = parse_args()

    ui = UserInterface(
        force=args.force,
        auto_login=args.login,
        source='./test_application.pkl' if args.test else './application.pkl'
    )

    ui.run()



if __name__ == "__main__":
    
    main()