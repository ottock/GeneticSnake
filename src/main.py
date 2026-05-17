from presentation.gui.app import run


def main() -> None:
    try:
        run()
    except Exception as e:
        raise e



if __name__ == "__main__":
    main()