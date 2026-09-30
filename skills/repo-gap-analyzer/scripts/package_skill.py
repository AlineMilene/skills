#!/usr/bin/env python3
"""
Packaging and distribution utility for the repo-gap-analyzer skill.

Validates the skill folder, builds compressed release bundles (.zip and .tar.gz),
and outputs SHA-256 checksums.

Usage:
    python scripts/package_skill.py
    python scripts/package_skill.py --out-dir dist --version 1.2.0
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

def calculate_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def package_skill(skill_dir: Path, out_dir: Path, version: str = None) -> bool:
    skill_dir = skill_dir.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Read metadata from skill.json if available
    manifest_path = skill_dir / "skill.json"
    if not version and manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                version = data.get("version", "1.0.0")
        except Exception:
            version = "1.0.0"
    version = version or "1.0.0"

    print(f"[*] Packaging skill: repo-gap-analyzer v{version}")
    print(f"[*] Source directory: {skill_dir}")
    print(f"[*] Output directory: {out_dir}")

    # 2. Run validate_skill.py
    validator_script = skill_dir / "scripts" / "validate_skill.py"
    if validator_script.exists():
        print("[*] Running pre-packaging validation...")
        cmd = [sys.executable, str(validator_script), str(skill_dir), "--format", "json"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("[!] Validation FAILED. Cannot package invalid skill.")
            print(proc.stdout or proc.stderr)
            return False
        print("[+] Validation PASSED successfully.")

    # 3. Create ZIP archive
    zip_filename = out_dir / f"repo-gap-analyzer-v{version}.zip"
    print(f"[*] Creating ZIP: {zip_filename.name}...")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in skill_dir.rglob("*"):
            if file.is_file() and not file.name.endswith(".pyc") and "__pycache__" not in file.parts:
                arcname = Path("repo-gap-analyzer") / file.relative_to(skill_dir)
                zipf.write(file, arcname)

    zip_hash = calculate_sha256(zip_filename)
    (out_dir / f"{zip_filename.name}.sha256").write_text(f"{zip_hash}  {zip_filename.name}\n", encoding="utf-8")
    print(f"[+] ZIP created: {zip_filename.name} (SHA-256: {zip_hash[:16]}...)")

    # 4. Create TAR.GZ archive
    tar_filename = out_dir / f"repo-gap-analyzer-v{version}.tar.gz"
    print(f"[*] Creating TAR.GZ: {tar_filename.name}...")
    with tarfile.open(tar_filename, "w:gz") as tarf:
        for file in skill_dir.rglob("*"):
            if file.is_file() and not file.name.endswith(".pyc") and "__pycache__" not in file.parts:
                arcname = Path("repo-gap-analyzer") / file.relative_to(skill_dir)
                tarf.add(file, arcname=str(arcname).replace("\\", "/"))

    tar_hash = calculate_sha256(tar_filename)
    (out_dir / f"{tar_filename.name}.sha256").write_text(f"{tar_hash}  {tar_filename.name}\n", encoding="utf-8")
    print(f"[+] TAR.GZ created: {tar_filename.name} (SHA-256: {tar_hash[:16]}...)")

    print("\n[+] Release artifacts generated successfully in:", out_dir)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package repo-gap-analyzer for distribution")
    parser.add_argument("--skill-dir", default=None, help="Path to repo-gap-analyzer folder")
    parser.add_argument("--out-dir", default=None, help="Output directory for packages")
    parser.add_argument("--version", help="Override release version")
    args = parser.parse_args()

    default_skill_dir = Path(__file__).resolve().parent.parent
    skill_dir = Path(args.skill_dir) if args.skill_dir else default_skill_dir
    default_out_dir = default_skill_dir.parent.parent / "dist"
    out_dir = Path(args.out_dir) if args.out_dir else default_out_dir

    success = package_skill(skill_dir, out_dir, args.version)
    sys.exit(0 if success else 1)
