"""confmerge.py：多层配置合并（基线：浅覆盖，无策略、无审计）。"""
from __future__ import annotations


class ConfigMerger:
    def __init__(self):
        self.layers = []
        self.audit = []
        self.unknown = []

    def load(self, name: str, data: dict) -> dict:
        self.layers.append((name, dict(data)))
        return {"layers": len(self.layers)}

    def merged(self) -> dict:
        """基线：键直接覆盖，嵌套字典整块替换。"""
        result = {}
        for _, data in self.layers:
            result.update(data)
        return result

    def merge_lists(self, policy: str) -> dict:
        raise NotImplementedError("列表策略还没实现")

    def validate(self, schema: dict) -> dict:
        raise NotImplementedError("类型校验还没实现")

    def diff(self, left: str, right: str) -> dict:
        """基线：只比顶层键集合。"""
        names = [name for name, _ in self.layers]
        a = dict(self.layers[names.index(left)][1])
        b = dict(self.layers[names.index(right)][1])
        return {"changed": sorted(set(a) & set(b)), "only_left": sorted(set(a) - set(b)),
                "only_right": sorted(set(b) - set(a))}

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"layers": len(self.layers), "audit": len(self.audit), "unknown": list(self.unknown)}
