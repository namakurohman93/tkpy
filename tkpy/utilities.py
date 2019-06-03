from .driver import Lobby
import argparse


def arg_parser():
    parser = argparse.ArgumentParser(usage='python3 %(prog)s <email> <password> <gameworld> [--avatar]')

    parser.add_argument('email', metavar='email', type=str, help='your email', nargs=1)
    parser.add_argument('password', metavar='password', type=str, help='your password', nargs=1)
    parser.add_argument('gameworld', metavar='gameworld', type=str, help='gameworld name', nargs=1)
    parser.add_argument('--avatar', help='your avatar', type=str, default=None, nargs='*')

    args = parser.parse_args()

    email = args.email[0]
    password = args.password[0]
    gameworld = args.gameworld[0]

    avatar = ' '.join(args.avatar) if args.avatar else None

    return email, password, gameworld, avatar


def login(email, password, gameworld, avatar=None):
    lobby = Lobby()
    lobby.authenticate(email, password)
    client = lobby.get_gameworld(gameworld, avatar)
    return client
