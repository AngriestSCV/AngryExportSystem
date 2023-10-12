#!/usr/bin/env python

import pathlib
try:
    import config_loader
except:
    from . import config_loader

def path_to_unity_path(cfg: config_loader.Config, path: str):
    start_path = pathlib.PurePath(path)
    u_path = cfg.get_unity_path()

    if not start_path.is_absolute(): raise ValueError(f"path must be absolute. Found: {start_path}")
    if not u_path.is_absolute(): raise ValueError(f"unity path must be absolute. Found: {start_path}")

    rel_path = start_path.relative_to(cfg.get_unity_path())
    return str(rel_path)
