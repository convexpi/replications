"""Discover every replication in the catalog."""
from __future__ import annotations
import importlib, pkgutil
from .base import Replication
from . import catalog


def all_replications() -> dict[str, Replication]:
    reps: dict[str, Replication] = {}
    for _, modname, _ in pkgutil.iter_modules(catalog.__path__):
        mod = importlib.import_module(f"{catalog.__name__}.{modname}")
        for obj in vars(mod).values():
            if isinstance(obj, type) and issubclass(obj, Replication) and obj is not Replication:
                inst = obj()
                reps[inst.name] = inst
    return dict(sorted(reps.items()))
