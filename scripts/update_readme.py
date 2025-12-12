#!/usr/bin/env python3
"""Generate the auto-updated summary section inside README.md."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
MARKER_START = "<!-- AUTO-GENERATED:START -->"
MARKER_END = "<!-- AUTO-GENERATED:END -->"
IGNORED_DIRS = {".git", "scripts", "__pycache__"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".webm", ".mkv"}


def slug_to_title(slug: str) -> str:
    words = slug.replace("_", " ").replace("-", " ").split()
    return " ".join(w.capitalize() for w in words) or slug


def load_metadata(example_dir: Path) -> Dict[str, Any]:
    meta_path = example_dir / "metadata.json"
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def find_case_insensitive(example_dir: Path, filename: str) -> Path | None:
    target = filename.lower()
    for item in example_dir.iterdir():
        if item.is_file() and item.name.lower() == target:
            return item
    return None


def extract_title(readme_path: Path | None, fallback: str) -> str:
    if readme_path and readme_path.exists():
        for raw in readme_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip() or fallback
    return slug_to_title(fallback)


def extract_description(readme_path: Path | None) -> str:
    if not readme_path or not readme_path.exists():
        return ""
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    desc_lines: List[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            if desc_lines:
                break
            continue
        if line.startswith("#"):
            continue
        if set(line) <= {"-", "—", "_"}:
            continue
        desc_lines.append(line)
    return " ".join(desc_lines)


def categorize_files(example_dir: Path) -> Dict[str, List[str]]:
    inputs: List[str] = []
    outputs: List[str] = []
    core: List[str] = []
    for item in example_dir.iterdir():
        if not item.is_file():
            continue
        name_lower = item.name.lower()
        if name_lower.startswith("input"):
            inputs.append(item.name)
        elif name_lower.startswith("output"):
            outputs.append(item.name)
        elif (
            name_lower.startswith("prompt")
            or name_lower.endswith("flow.json")
            or name_lower.endswith("code.py")
        ):
            core.append(item.name)
    inputs.sort()
    outputs.sort()
    core.sort()
    return {"inputs": inputs, "outputs": outputs, "core": core}


def is_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in IMAGE_EXTS


def is_video(filename: str) -> bool:
    return Path(filename).suffix.lower() in VIDEO_EXTS


def guess_type(filename: str) -> str:
    if is_image(filename):
        return "image"
    if is_video(filename):
        return "video"
    return "file"


def normalize_assets(meta_value: Any, fallback_files: List[str]) -> List[Dict[str, str]]:
    if isinstance(meta_value, list) and meta_value:
        assets: List[Dict[str, str]] = []
        for item in meta_value:
            if isinstance(item, str):
                assets.append({"file": item, "label": "", "type": guess_type(item)})
            elif isinstance(item, dict):
                file_name = item.get("file")
                if not file_name:
                    continue
                assets.append(
                    {
                        "file": file_name,
                        "label": item.get("label", ""),
                        "type": item.get("type") or guess_type(file_name),
                    }
                )
        if assets:
            return assets
    return [{"file": name, "label": "", "type": guess_type(name)} for name in fallback_files]


def normalize_core(meta_value: Any, fallback_files: List[str]) -> List[str]:
    if isinstance(meta_value, list) and meta_value:
        core_files: List[str] = []
        for item in meta_value:
            if isinstance(item, str):
                core_files.append(item)
            elif isinstance(item, dict) and item.get("file"):
                core_files.append(item["file"])
        if core_files:
            return core_files
    return fallback_files


def gather_example(example_dir: Path, platform_name: str, platform_title: str) -> Dict[str, Any]:
    readme_path = find_case_insensitive(example_dir, "README.md")
    metadata = load_metadata(example_dir)
    files = categorize_files(example_dir)
    title = metadata.get("title") or extract_title(readme_path, example_dir.name)
    description = metadata.get("description") or extract_description(readme_path)
    rel_path = example_dir.relative_to(ROOT)
    doc_path = readme_path.relative_to(ROOT) if readme_path else ""
    return {
        "platform": platform_name,
        "platform_title": platform_title,
        "title": title,
        "description": description or "（说明待补充）",
        "path": str(rel_path),
        "doc": str(doc_path) if doc_path else "",
        "inputs": normalize_assets(metadata.get("inputs"), files["inputs"]),
        "outputs": normalize_assets(metadata.get("outputs"), files["outputs"]),
        "core": normalize_core(metadata.get("core"), files["core"]),
    }


def gather_data() -> List[Dict[str, Any]]:
    examples: List[Dict[str, Any]] = []
    for platform_dir in sorted(ROOT.iterdir()):
        if not platform_dir.is_dir() or platform_dir.name in IGNORED_DIRS:
            continue
        for example_dir in sorted(platform_dir.iterdir()):
            if not example_dir.is_dir():
                continue
            examples.append(
                gather_example(example_dir, platform_dir.name, slug_to_title(platform_dir.name))
            )
    return examples


def format_list(items: List[str]) -> str:
    return ", ".join(f"`{item}`" for item in items) if items else "（未提供）"


def render_section(examples: List[Dict[str, Any]]) -> str:
    if not examples:
        return "_暂未收录任何示例_\n"
    lines: List[str] = []
    lines.append("| 模型（平台） | 说明 | 输入 | 输出 | Prompt | 文件夹 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for example in examples:
        platform_cell = (
            f"{example['platform_title']}<br><strong>{example['title']}</strong>"
        )
        inputs_cell = render_assets_cell(example["inputs"], example["path"])
        outputs_cell = render_assets_cell(example["outputs"], example["path"])
        prompt_cell = render_core_cell(example["core"], example["path"])
        folder_cell = render_folder_cell(example["path"], example.get("doc", ""))
        desc = example["description"]
        lines.append(
            f"| {platform_cell} | {desc} | {inputs_cell} | {outputs_cell} | {prompt_cell} | {folder_cell} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_assets_cell(assets: List[Dict[str, str]], example_path: str) -> str:
    if not assets:
        return "（未提供）"
    parts: List[str] = []
    for asset in assets:
        file_name = asset["file"]
        label = asset.get("label") or ""
        display = f"`{file_name}`"
        if label:
            display = f"{label}（`{file_name}`）"
        addition = ""
        rel = (Path(example_path) / file_name).as_posix()
        if asset.get("type") == "image":
            addition = f"<br>![{label or file_name}]({rel})"
        elif asset.get("type") == "video":
            addition = f"<br>[查看视频]({rel})"
        parts.append(display + addition)
    return "<br><br>".join(parts)


def render_core_cell(core_files: List[str], example_path: str) -> str:
    if not core_files:
        return "（未提供）"
    links = []
    for file_name in core_files:
        rel = (Path(example_path) / file_name).as_posix()
        links.append(f"[{file_name}]({rel})")
    return "<br>".join(links)


def render_folder_cell(example_path: str, doc_path: str) -> str:
    links = [f"[文件夹]({example_path})"]
    if doc_path:
        links.append(f"[README]({doc_path})")
    return "<br>".join(links)


def replace_section(readme_text: str, new_section: str) -> str:
    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        raise SystemExit("README.md 中缺少自动生成标记。")
    start = readme_text.index(MARKER_START)
    end = readme_text.index(MARKER_END) + len(MARKER_END)
    replacement = f"{MARKER_START}\n{new_section}{MARKER_END}"
    return readme_text[:start] + replacement + readme_text[end:]


def main() -> None:
    platforms = gather_data()
    section = render_section(platforms)
    readme_text = README_PATH.read_text(encoding="utf-8")
    updated = replace_section(readme_text, section)
    README_PATH.write_text(updated, encoding="utf-8")
    print("README.md 已更新。")


if __name__ == "__main__":
    main()
