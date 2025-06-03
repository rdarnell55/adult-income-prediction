import tarfile

with tarfile.open("model.tar.gz", "w:gz") as tar:
    tar.add("model.pkl", arcname="model.pkl")

print("model.tar.gz created successfully.")