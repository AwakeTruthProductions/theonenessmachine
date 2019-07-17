import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def print_banner(banner_text):
    print(banner_text)

if __name__ == "__main__":
    banner_text = open(os.path.join(__location__, 'banner.txt'), 'r').read()
    print_banner(banner_text)
