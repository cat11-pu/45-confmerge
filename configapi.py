"""configapi.py：对外门面（老接口 load/merged/diff 不能改）。"""
from __future__ import annotations

from confmerge import ConfigMerger


class Config:
    def __init__(self):
        self.merger = ConfigMerger()

    def load(self, name: str, data: dict) -> dict:
        return self.merger.load(name, data)

    def merged(self, policy: str = "replace") -> dict:
        self.merger.merge_lists(policy)
        return self.merger.merged()

    def validate(self, schema: dict) -> dict:
        return self.merger.validate(schema)

    def snapshot(self) -> bytes:
        return self.merger.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.merger.restore(blob)
