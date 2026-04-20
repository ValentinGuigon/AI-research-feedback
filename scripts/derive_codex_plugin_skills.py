from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SKILLS_DIR = REPO_ROOT / "Skills"
PLUGIN_SKILLS_DIR = REPO_ROOT / "plugins" / "ai-research-feedback" / "skills"
EXPECTED_SKILLS = [
    "fetch-grant-context",
    "plan-grant-review",
    "review-paper",
    "review-paper-light",
    "review-paper-code",
    "review-pap",
    "review-grant",
]


def write_if_changed(path: Path, content: bytes) -> bool:
    if path.exists() and path.read_bytes() == content:
        return False
    path.write_bytes(content)
    return True


def main() -> int:
    if not CANONICAL_SKILLS_DIR.exists():
        raise FileNotFoundError(f"Missing canonical skills directory: {CANONICAL_SKILLS_DIR}")

    PLUGIN_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # Keep the plugin surface exact: one directory per expected canonical skill.
    for child in PLUGIN_SKILLS_DIR.iterdir():
        if child.is_dir() and child.name not in EXPECTED_SKILLS:
            shutil.rmtree(child)

    changed = False
    for skill_name in EXPECTED_SKILLS:
        source_path = CANONICAL_SKILLS_DIR / f"{skill_name}.md"
        if not source_path.exists():
            raise FileNotFoundError(f"Missing canonical skill source: {source_path}")

        target_dir = PLUGIN_SKILLS_DIR / skill_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / "SKILL.md"

        changed = write_if_changed(
            target_path,
            source_path.read_bytes(),
        ) or changed

    print(f"Derived {len(EXPECTED_SKILLS)} plugin skills from canonical Skills/.")
    print(f"Changes written: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
