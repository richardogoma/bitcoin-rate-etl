#!/usr/bin/env python3
from etl import start_etl
from config import Config

config_instance = Config()

if __name__ == "__main__":
    start_etl(config_instance)
