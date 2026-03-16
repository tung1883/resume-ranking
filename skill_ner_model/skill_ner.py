import subprocess
import sys
import os

TRAIN_PATH = "./data/train.spacy"
DEV_PATH = "./data/dev.spacy"
CONFIG_PATH = "./config.cfg"
OUTPUT_DIR = "./output"

def create_config():
    if not os.path.exists(CONFIG_PATH):
        print("Creating spaCy config...")
        subprocess.run([
            sys.executable,
            "-m",
            "spacy",
            "init",
            "config",
            CONFIG_PATH,
            "--lang",
            "en",
            "--pipeline",
            "ner",
            "--optimize",
            "efficiency"
        ])


def train_model():
    print("Starting training...")

    subprocess.run([
        sys.executable,
        "-m",
        "spacy",
        "train",
        CONFIG_PATH,
        "--paths.train",
        TRAIN_PATH,
        "--paths.dev",
        DEV_PATH,
        "--output",
        OUTPUT_DIR
    ])


if __name__ == "__main__":
    create_config()
    train_model()
