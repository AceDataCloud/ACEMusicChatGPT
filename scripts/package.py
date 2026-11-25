"""Build the pinned Apps SDK source and package just its ACE Music profile."""

import argparse
import gzip
import hashlib
import io
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream"
PROFILE = "acemusic"
PACKAGE = "acemusic-chatgpt"


def build(output):
    revision = subprocess.check_output(
        ["git", "rev-parse", ":upstream"], cwd=ROOT, text=True
    ).strip()
    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp) / "source"
        work.mkdir()
        source = subprocess.check_output(
            ["git", "archive", "--format=tar", revision], cwd=UPSTREAM
        )
        with tarfile.open(fileobj=io.BytesIO(source)) as archive:
            archive.extractall(work, filter="data")
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=work, check=True)
        subprocess.run(["npm", "run", "build"], cwd=work, check=True)

        staging = Path(temp) / PACKAGE
        staging.mkdir()
        for filename in ("package.json", "package-lock.json", "LICENSE"):
            shutil.copyfile(work / filename, staging / filename)
        shutil.copytree(work / "src", staging / "src")
        shutil.copytree(work / "dist" / PROFILE, staging / "dist" / PROFILE)
        manifests = staging / "profiles" / PROFILE
        manifests.mkdir(parents=True)
        for filename in ("profile.json", "runtime.json"):
            shutil.copyfile(work / "profiles" / PROFILE / filename, manifests / filename)
        for filename in ("run.mjs", "INSTALL.md"):
            shutil.copyfile(ROOT / filename, staging / filename)
        (staging / "SOURCE_COMMIT").write_text(revision + "\n")

        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("wb") as raw, gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, mtime=0
        ) as compressed, tarfile.open(fileobj=compressed, mode="w") as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    data = path.read_bytes()
                    info = tarfile.TarInfo(str(path.relative_to(staging.parent)))
                    info.mode, info.size = 0o644, len(data)
                    archive.addfile(info, io.BytesIO(data))
    with output.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    print(f"{digest}  {output.name}")
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    build(parser.parse_args().output)
