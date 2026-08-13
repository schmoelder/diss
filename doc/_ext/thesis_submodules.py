from pathlib import Path

from git import Repo


def restore_pinned_submodule(repo_root: Path, submodule_path: str) -> None:
    """Check out the submodule commit recorded by the parent repository."""
    repo_root = Path(repo_root)
    pinned_commit = Repo(repo_root).git.rev_parse(f"HEAD:{submodule_path}")
    submodule_repo = Repo(repo_root / submodule_path)
    if submodule_repo.head.commit.hexsha != pinned_commit:
        submodule_repo.git.checkout(pinned_commit)
