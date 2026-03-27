import uuid
import random


CONFIG_DIRS = [
    "/config",
    "/private",
    "/system",
    "/backup"
]

FILE_NAMES = [
    "prod_admin_backup",
    "root_credentials",
    "internal_db_keys",
    "k8s_cluster_keys",
    "aws_root_credentials"
]

ENDPOINT_NAMES = [
    "admin-console",
    "debug-panel",
    "dev-backdoor",
    "internal-admin",
    "test-console"
]


def _random_suffix():
    return str(uuid.uuid4())[:4]


def generate_endpoint_traps(count=5):

    traps = []

    for _ in range(count):

        name = random.choice(ENDPOINT_NAMES)
        path = f"/{name}_{_random_suffix()}"

        traps.append(path)

    return traps


def generate_file_traps(count=5):

    traps = []
    tokens = []

    for _ in range(count):

        directory = random.choice(CONFIG_DIRS)
        name = random.choice(FILE_NAMES)

        suffix = _random_suffix()

        token = "HT_" + str(uuid.uuid4())[:8]

        path = f"{directory}/{name}_{suffix}.txt"

        content = f"""
# INTERNAL ADMIN CONFIG

username=backup_admin
password={token}

# DO NOT DELETE
# Used for emergency recovery
"""

        traps.append({
            "path": path,
            "content": content,
            "token": token
        })

        tokens.append(token)

    return traps, tokens