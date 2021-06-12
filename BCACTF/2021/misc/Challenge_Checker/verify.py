#!/usr/bin/env python3
from yaml import load
from termcolor import cprint
from pathlib import Path
from typing import Tuple
import sys

def check(raw_data) -> "Tuple[list[str], list[str]]":
    data = load(raw_data)
    if not isinstance(data, dict):
        raise Exception("Data must be a dictionary")

    errors = []
    warnings = []

    if "name" not in data:
        errors.append('Property "name" is missing')
    elif not isinstance(data["name"], str):
        errors.append('Property "name" must be a string')

    if "categories" not in data:
        errors.append('Property "categories" is missing')
    elif not isinstance(data["categories"], list):
        errors.append('Property "categories" must be a list')
    else:
        if len(data["categories"]) != len(set(data["categories"])):
            errors.append('Property "categories" contains duplicate items')
        for category in data["categories"]:
            if category not in ("misc", "binex", "crypto", "foren", "rev", "webex"):
                errors.append(f'Invalid value for {category}')

    if "tags" in data:
        if isinstance(data["tags"], list):
            if len(data["tags"]) != len(set(data["tags"])):
                errors.append('Property "tags" contains duplicate items')
            if len(set(data["tags"]) & set(data["categories"])) > 0:
                errors.append('Properties "categories" and "tags" contain duplicate items')
            for tag in data["tags"]:
                if not isinstance(tag, str):
                    errors.append(f'Tag {tag} must be a string')
        else:
            errors.append('Property "tags" must be a list')

    if "value" not in data:
        errors.append('Property "value" is missing')
    elif not isinstance(data["value"], int):
        errors.append('Property "value" must be an integer')

    if "flag" not in data:
        errors.append('Property "flag" is missing')
    elif isinstance(data["flag"], dict):
        if "file" not in data["flag"]:
            errors.append('Property "flag" must either be a string or a dictionary containing the "file" property')
        elif not isinstance(data["flag"]["file"], str):
            errors.append('Property "flag.file" must be a string')
    elif not isinstance(data["flag"], str):
        errors.append('Property "flag" must either be a string or a dictionary containing the "file" property')

    if "description" in data and not isinstance(data["description"], str):
        errors.append('Property "description" must be a string')

    if "hints" in data:
        if isinstance(data["hints"], list):
            if any(not isinstance(hint, str) for hint in data["hints"]):
                errors.append('Property "hints" must be a list of strings if it exists')
        else:
            errors.append('Property "hints" must be a list of strings if it exists')

    if "deploy" in data:
        if isinstance(data["deploy"], dict):
            for name, deploy in data["deploy"].items():
                if isinstance(deploy, dict):
                    if "build" not in deploy:
                        errors.append(f"Deployment {name}: Property \"build\" is missing")
                    elif not isinstance(deploy["build"], str):
                        errors.append(f"Deployment {name}: Property \"build\" must be a string")
                    if "environment" in deploy and not isinstance(deploy["environment"], dict):
                        errors.append(f"Deployment {name}: Property \"environment\" must be a dictionary")
                    if "expose" in deploy and not isinstance(deploy["expose"], int):
                        errors.append(f"Deployment {name}: Property \"expose\" must be an integer")
                else:
                    errors.append(f"Deployment {name}: Must be a dictionary")
        else:
            errors.append('Property "deploy" must be a dictionary')

    if "files" in data:
        if isinstance(data["files"], list):
            for i, file in enumerate(data["files"]):
                filename = str(i + 1)
                if isinstance(file, dict):
                    if "src" not in file:
                        errors.append(f"File {filename}: Property \"src\" is missing")
                    elif not isinstance(file["src"], str):
                        errors.append(f"File {filename}: Property \"src\" must be a string")
                    else:
                        filename = f"\"{file['src'].encode('utf8').decode('unicode_escape')}\""
                        if "container" in file:
                            if "deploy" not in data:
                                errors.append(f"File {filename}: Uses file from container but \"deploy\" does not exist")
                            elif file["container"] not in data["deploy"]:
                                errors.append(f"File {filename}: Deployment {file['container']} not in \"deploy\" section")
                    if "name" in file and not isinstance(file["name"], str):
                        errors.append(f'File {filename}: Property "name" must be a string')
                else:
                    errors.append(f'File {filename}: Must be a dictionary')
        else:
            errors.append('Property "files" must be a list of strings')

    if "authors" not in data:
        errors.append('Property "authors" is missing')
    elif isinstance(data["authors"], str):
        errors.append('Property "authors" must be a list of strings, not a string *cough cough anli*')
    elif not isinstance(data["authors"], list):
        errors.append('Property "authors" must be a list of strings')
    elif len(data["authors"]) == 0:
        errors.append('Property "authors" must have at least one element')
    elif any(not isinstance(author, str) for author in data["authors"]):
        errors.append('Property "authors" must be a list of strings')

    if "visible" in data and not isinstance(data["visible"], bool):
        errors.append('Property "visible" must be a boolean')

    return errors, warnings

if __name__ == "__main__":
    cprint("Paste in your chall.yaml file, then send an EOF or two empty lines:", "cyan", attrs=["bold"])
    sys.stdout.flush()
    try:
        raw_data = ""
        empty_lines = 0
        while empty_lines < 2:
            try:
                line = input()
            except EOFError:
                break
            if len(line) > 0:
                empty_lines = 0
            else:
                empty_lines += 1
            raw_data += line + "\n"
        errors, warnings = check(raw_data)
    except Exception as e:
        cprint("Fatal error: ", "red", attrs=["bold"], end="")
        print(e)
        exit(1)

    if len(errors) > 0:
        cprint(f"{len(errors)} error(s) found", "red", attrs=["bold"])
        for error in errors:
            print(error)
    
    if len(warnings) > 0:
        cprint(f"{len(warnings)} warning(s) found", "yellow", attrs=["bold"])
        for warning in warnings:
            print(warning)
    
    if len(errors) > 0:
        exit(1)
    elif len(warnings) == 0:
        cprint("No issues found", "green", attrs=["bold"])
