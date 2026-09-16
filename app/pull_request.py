from app.github_client import get_repository


def get_pull_request(pr_number: int):
    repo = get_repository()
    return repo.get_pull(pr_number)


def get_changed_files(pr_number: int):
    pr = get_pull_request(pr_number)
    repo = get_repository()

    changed_files = []

    for file in pr.get_files():
        content = None

        if file.status != "removed":
            try:
                file_content = repo.get_contents(
                    file.filename,
                    ref=pr.head.sha
                )

                content = file_content.decoded_content.decode("utf-8")

            except Exception as e:
                print(f"Could not fetch {file.filename}: {e}")

        changed_files.append({
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "patch": file.patch,
            "content": content
        })

    return changed_files