import os
import re
import httpx
import tempfile
import zipfile

# Extensions that are likely binary or we want to skip
SKIP_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".mp4",
    ".webm",
    ".ogg",
    ".mp3",
    ".wav",
    ".ttf",
    ".woff",
    ".woff2",
    ".eot",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".dat",
    ".db",
    ".sqlite",
    ".pyc",
    ".class",
    ".jar",
    ".war",
    ".ear",
    ".pkl",
}

# Directories we definitely want to skip
SKIP_DIRECTORIES = {
    "node_modules",
    ".git",
    ".github",
    "venv",
    "env",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "out",
    "target",
    ".next",
    ".cache",
    "vendor",
    "bower_components",
}

MAX_FILE_SIZE = 50 * 1024  # Skip files larger than 50KB to save tokens
MAX_TOTAL_SIZE = 1 * 1024 * 1024  # Max 1MB of text context


async def fetch_github_repo_context(url: str) -> str:
    """
    Given a GitHub URL, downloads the default branch's zipball,
    extracts it, and returns a concatenated string of the source code files.
    """
    # 1. Parse URL to get owner and repo
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/?", url)
    if not match:
        raise ValueError(
            "Invalid GitHub repository URL. Must be in format https://github.com/owner/repo"
        )

    owner, repo = match.groups()
    repo = repo.replace(".git", "")

    zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    # 2. Download the zip
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(zip_url, headers={"User-Agent": "CodeMentorAI"})
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch repository. GitHub API returned status {response.status_code}. Make sure it is a public repository."
            )

        zip_content = response.content

    # 3. Process the zip in a temporary directory
    context = []
    total_size = 0

    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "repo.zip")
        with open(zip_path, "wb") as f:
            f.write(zip_content)

        extract_dir = os.path.join(temp_dir, "extract")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # 4. Traverse and concatenate
        for root, dirs, files in os.walk(extract_dir):
            # Prune skip directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SKIP_EXTENSIONS:
                    continue

                file_path = os.path.join(root, file)

                # Check file size
                if os.path.getsize(file_path) > MAX_FILE_SIZE:
                    continue

                # Calculate relative path (ignoring the random root dir created by github zip)
                rel_path = os.path.relpath(file_path, extract_dir)
                # GitHub zip has a top-level dir like `owner-repo-commitHash`
                parts = rel_path.split(os.sep)
                if len(parts) > 1:
                    clean_rel_path = os.path.join(*parts[1:])
                else:
                    clean_rel_path = rel_path

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        if total_size + len(content) > MAX_TOTAL_SIZE:
                            context.append(
                                f"\n\n--- STOPPED --- (Reached Maximum Context Limit of {MAX_TOTAL_SIZE // 1024}KB)"
                            )
                            break

                        total_size += len(content)

                        file_ext = ext.replace(".", "")
                        context.append(
                            f"File: {clean_rel_path}\n```{file_ext}\n{content}\n```\n"
                        )
                except UnicodeDecodeError:
                    # Likely a binary file that we missed by extension, skip it
                    continue

            if total_size > MAX_TOTAL_SIZE:
                break

    return "\n".join(context)
