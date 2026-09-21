import json

from app.security_analyzer import run_bandit
from app.static_analyzer import run_ruff


def review_code(changed_files):
    reviews = []

    for file in changed_files:
        filename = file["filename"]
        content = file.get("content")

        file_review = []

        if content is not None:
            # -------------------------
            # Ruff: Code quality
            # -------------------------
            ruff_result = run_ruff(filename, content)

            if ruff_result:
                try:
                    issues = json.loads(ruff_result)

                    for issue in issues:
                        message = issue.get("message", "Unknown issue")
                        location = issue.get("location", {})

                        row = location.get("row")
                        column = location.get("column")

                        file_review.append(
                            f"❌ Ruff: {message} "
                            f"(line {row}, column {column})"
                        )

                except json.JSONDecodeError:
                    file_review.append(
                        f"❌ Ruff found an issue:\n{ruff_result}"
                    )

            # -------------------------
            # Bandit: Security
            # -------------------------
            bandit_result = run_bandit(filename, content)

            if bandit_result:
                try:
                    bandit_data = json.loads(bandit_result)

                    for issue in bandit_data.get("results", []):
                        test_id = issue.get("test_id", "Unknown")
                        message = issue.get("issue_text", "Unknown issue")
                        severity = issue.get("issue_severity", "UNKNOWN")
                        confidence = issue.get(
                            "issue_confidence",
                            "UNKNOWN"
                        )

                        line = issue.get("line_number", "?")

                        file_review.append(
                            f"🔒 Bandit {test_id}: {message} "
                            f"(severity: {severity}, "
                            f"confidence: {confidence}, "
                            f"line {line})"
                        )

                except json.JSONDecodeError:
                    file_review.append(
                        f"🔒 Bandit found a security issue:\n"
                        f"{bandit_result}"
                    )

        if file_review:
            reviews.append(
                f"### Review for `{filename}`\n\n"
                + "\n".join(
                    f"- {issue}" for issue in file_review
                )
            )
        else:
            reviews.append(
                f"### Review for `{filename}`\n\n"
                "✅ No issues detected by the static analyzer."
            )

    return "\n\n".join(reviews)