
import os
import json
import subprocess
from pathlib import Path

def clone_repo(repo_url, clone_dir):
    if not clone_dir.exists():
        subprocess.run(["git", "clone", repo_url, str(clone_dir)], check=True)
    else:
        subprocess.run(["git", "-C", str(clone_dir), "pull"], check=True)

def extract_files(base_path):
    model_path = base_path / "app" / "models.py"
    route_path = base_path / "app" / "routes.py"
    content = ""
    if model_path.exists():
        content += model_path.read_text() + "\n\n"
    if route_path.exists():
        content += route_path.read_text()
    return content.strip()

def main(input_file, output_file):
    with open(input_file, "r") as f:
        entries = json.load(f)

    data = []
    output_dir = Path("cloned_repos")
    output_dir.mkdir(exist_ok=True)

    for entry in entries:
        prompt = entry["prompt"]
        repo_url = entry["git_repo"]
        repo_name = repo_url.split("/")[-1]
        clone_path = output_dir / repo_name

        try:
            clone_repo(repo_url, clone_path)
            target_code = extract_files(clone_path)
            if target_code:
                data.append({"inputs": prompt, "targets": target_code})
        except Exception as e:
            print(f"Failed to process {repo_url}: {e}")

    with open(output_file, "w") as out_f:
        for item in data:
            out_f.write(json.dumps(item) + "\n")

if __name__ == "__main__":
    main("input_repos.json", "codet5_training_data.jsonl")
