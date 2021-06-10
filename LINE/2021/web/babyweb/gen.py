from uuid import uuid4


USERNAME_HEADER = f"x-user-{uuid4()}"
PASSWORD_HEADER = f"x-pass-{uuid4()}"

USERNAME_ADMIN = "admin"
PASSWORD_ADMIN = f"{uuid4()}"

with open("docker-compose_tmp.yml") as f:
    dcyml = f.read()

dcyml = dcyml.replace("USERNAME_HEADER_DUMMY", USERNAME_HEADER)
dcyml = dcyml.replace("PASSWORD_HEADER_DUMMY", PASSWORD_HEADER)
dcyml = dcyml.replace("USERNAME_ADMIN_DUMMY", USERNAME_ADMIN)
dcyml = dcyml.replace("PASSWORD_ADMIN_DUMMY", PASSWORD_ADMIN)

with open("docker-compose.yml", "w") as f:
    f.write(dcyml)
