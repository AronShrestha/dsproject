"""
"""
from __future__ import annotations

import fire  # type: ignore
from salesapi import console


if __name__ == "__main__":
    fire.Fire(console.CliCommand)
