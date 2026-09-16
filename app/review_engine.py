from app.static_analyzer import run_ruff
import json


def review_code(changed_files):
    reviews = []

    for file in changed_files:
        filename = file["filename"]
        content = file.get("content")

        file_review = []

        # Run Ruff on the complete file
        if content is not None:
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

        if file_review:
            reviews.append(
                f"### Review for `{filename}`\n\n"
                + "\n".join(f"- {issue}" for issue in file_review)
            )
        else:
            reviews.append(
                f"### Review for `{filename}`\n\n"
                "✅ No issues detected by the static analyzer."
            )

    return "\n\n".join(reviews)