"""
The main entry point. Invoke as `compare_reqs' or `python -m compare_reqs'.
"""


def main():
    try:
        from compare_reqs.core import main
        exit_status = main()
    except KeyboardInterrupt:
        from compare_reqs.status import ExitStatus
        exit_status = ExitStatus.ERROR_CTRL_C

    return exit_status.value


if __name__ == '__main__':
    import sys
    sys.exit(main())
