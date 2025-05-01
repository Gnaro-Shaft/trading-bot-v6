# version_manager.py

def get_version():
    with open("version.txt", "r") as f:
        return f.read().strip()

def bump_version():
    current = get_version()
    major, minor = map(int, current.split("."))
    minor += 1
    new_version = f"{major}.{minor}"
    with open("version.txt", "w") as f:
        f.write(new_version)
    return new_version
