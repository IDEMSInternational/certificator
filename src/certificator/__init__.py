def api_version():
    try:
        from certificator._version import version
    except ModuleNotFoundError:
        version = "dev"

    return version
