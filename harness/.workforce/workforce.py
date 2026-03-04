#!/usr/bin/env python3
"""Onboard and offboard local agent workspaces for this repository."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple

WORKFORCE_DIR = Path(__file__).resolve().parent          # harness/.workforce/
ROOT = WORKFORCE_DIR.parent                              # harness/
REPO_ROOT = ROOT.parent                                  # project root (one level above harness/)
TEMPLATES_DIR = WORKFORCE_DIR / "templates"
SKILLS_SOURCE_DIR = WORKFORCE_DIR / "agent-template" / "skills"
AUTO_HEADER = "<!-- AUTO-GENERATED: DO NOT EDIT -->"
REQUIRED_MANIFEST_FIELDS = (
    "agent_name",
    "context_folder",
    "primary_file",
    "native_init",
    "skills_library_sync",
)


class WorkforceError(RuntimeError):
    """Raised when onboarding data is invalid."""


def parse_manifest(path: Path) -> Dict[str, str]:
    """Parse a small key/value YAML file without external dependencies."""
    data: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise WorkforceError(f"Invalid manifest line in {path}: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def load_manifest(agent: str) -> Tuple[Dict[str, str], Path]:
    template_dir = TEMPLATES_DIR / agent
    manifest_path = template_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise WorkforceError(f"Unknown agent template: {agent}")
    manifest = parse_manifest(manifest_path)
    missing = [name for name in REQUIRED_MANIFEST_FIELDS if name not in manifest]
    if missing:
        raise WorkforceError(
            f"Manifest {manifest_path} missing required fields: {', '.join(missing)}"
        )
    return manifest, template_dir


def resolve_target_dir(manifest: Dict[str, str]) -> Path:
    folder = manifest["context_folder"].strip()
    if not folder:
        raise WorkforceError("Manifest field `context_folder` cannot be empty")
    return REPO_ROOT / folder


def run_native_init(command: str, dry_run: bool) -> None:
    if not command or command.lower() == "none":
        return
    if dry_run:
        print(f"[dry-run] would run native init: {command}")
        return
    completed = subprocess.run(command, shell=True, cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        print(
            f"warning: native init command exited with code {completed.returncode}: {command}",
            file=sys.stderr,
        )


def write_primary_file(
    manifest: Dict[str, str], template_dir: Path, target_dir: Path, dry_run: bool
) -> None:
    primary_rel = manifest["primary_file"].strip()
    if not primary_rel:
        raise WorkforceError("Manifest field `primary_file` cannot be empty")

    template_path = template_dir / "AGENTS.md"
    if not template_path.exists():
        raise WorkforceError(f"Missing template file: {template_path}")

    output_path = target_dir / primary_rel
    content = f"{AUTO_HEADER}\n\n{template_path.read_text(encoding='utf-8').rstrip()}\n"
    if dry_run:
        print(f"[dry-run] would write {output_path}")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def sync_skills(mode: str, target_dir: Path, dry_run: bool) -> None:
    if not SKILLS_SOURCE_DIR.exists():
        raise WorkforceError(f"Skills source folder not found: {SKILLS_SOURCE_DIR}")

    if dry_run:
        print(
            f"[dry-run] would sync skills from {SKILLS_SOURCE_DIR} to {target_dir} via {mode}"
        )
        return

    if target_dir.exists() or target_dir.is_symlink():
        if target_dir.is_symlink() or target_dir.is_file():
            target_dir.unlink()
        else:
            shutil.rmtree(target_dir)

    if mode == "symlink":
        try:
            target_dir.symlink_to(SKILLS_SOURCE_DIR, target_is_directory=True)
            return
        except OSError:
            print(
                "warning: symlink creation failed, falling back to copy mode",
                file=sys.stderr,
            )

    shutil.copytree(SKILLS_SOURCE_DIR, target_dir)


def prompt_existing_folder(target_dir: Path) -> str:
    while True:
        answer = input(
            f"Target folder already exists: {target_dir}\nChoose [R]eset or [S]kip: "
        ).strip().lower()
        if answer in {"r", "s"}:
            return answer
        print("Invalid choice. Enter 'R' or 'S'.")


def cmd_hire(args: argparse.Namespace) -> int:
    manifest, template_dir = load_manifest(args.agent)
    target_dir = resolve_target_dir(manifest)

    if target_dir.exists():
        if args.reset:
            action = "r"
        elif args.skip_existing:
            action = "s"
        elif not sys.stdin.isatty():
            raise WorkforceError(
                "Target folder exists in non-interactive mode. Use --reset or --skip-existing."
            )
        else:
            action = prompt_existing_folder(target_dir)

        if action == "s":
            print(f"skip: {target_dir} already exists")
            return 0
        if args.dry_run:
            print(f"[dry-run] would delete {target_dir}")
        else:
            shutil.rmtree(target_dir)

    if args.dry_run:
        print(f"[dry-run] would create {target_dir}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    run_native_init(manifest["native_init"], args.dry_run)
    write_primary_file(manifest, template_dir, target_dir, args.dry_run)
    sync_skills(
        manifest["skills_library_sync"].strip().lower(),
        target_dir / "skills",
        args.dry_run,
    )
    print(f"hired: {manifest['agent_name']} -> {target_dir}")
    return 0


def cmd_fire(args: argparse.Namespace) -> int:
    manifest, _ = load_manifest(args.agent)
    target_dir = resolve_target_dir(manifest)
    if not target_dir.exists():
        print(f"not onboarded: {manifest['agent_name']} ({target_dir} not found)")
        return 0

    if args.dry_run:
        print(f"[dry-run] would delete {target_dir}")
        return 0

    shutil.rmtree(target_dir)
    print(f"fired: {manifest['agent_name']} -> removed {target_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage local agent onboarding via hire/fire commands."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hire_parser = subparsers.add_parser("hire", help="Create and configure an agent folder")
    hire_parser.add_argument("agent", help="Agent template name, e.g. gemini")
    hire_parser.add_argument(
        "--dry-run", action="store_true", help="Show planned actions without writing files"
    )
    hire_parser.add_argument(
        "--reset", action="store_true", help="Delete and recreate existing target folder"
    )
    hire_parser.add_argument(
        "--skip-existing", action="store_true", help="Exit successfully if target exists"
    )
    hire_parser.set_defaults(func=cmd_hire)

    fire_parser = subparsers.add_parser("fire", help="Remove an onboarded agent folder")
    fire_parser.add_argument("agent", help="Agent template name, e.g. gemini")
    fire_parser.add_argument(
        "--dry-run", action="store_true", help="Show planned actions without deleting files"
    )
    fire_parser.set_defaults(func=cmd_fire)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except WorkforceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
