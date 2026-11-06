"""
LIHUA GUARD AI
Main controller

Version: 0.2
"""

from core.system import LihuaSystem


def main():
    lihua = LihuaSystem()

    lihua.start()


if __name__ == "__main__":
    main()