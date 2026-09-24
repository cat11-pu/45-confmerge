"""check_sample.py：按 sample/layers.json 走一圈，打印验收面。"""
import json
import os
import sys

from confmerge import ConfigMerger


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "layers.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    merger = ConfigMerger()
    for name in ("base", "region", "prod"):
        merger.load(name, spec["layers"][name])
    deep = merger.merged()
    merger.merge_lists(spec["policy"])
    with_policy = merger.merged()
    report = merger.validate(spec["schema"])
    blob = merger.persist()
    reborn = ConfigMerger()
    restored = reborn.restore(blob)
    print("深合并结果 =", deep)
    print("列表策略（%s）后的列表 =" % spec["policy"], with_policy.get("upstreams"))
    print("类型校验的错误 =", report.get("errors"))
    print("未知键 =", report.get("unknown"))
    print("嵌套键是否保留 =", spec["nested_kept"])
    print("每一层的贡献键 =", spec["layer_contrib"])
    print("恢复后的层数 =", restored.get("layers"))
    print("不变量（最终值都能指到某一层） =", spec["provenance_invariant"])
    print("层数 =", len(spec["layers"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
