import os, json, time
import requests
from openai import OpenAI

model     = os.environ["AI_MODEL"]
gh_token  = os.environ["GITHUB_TOKEN"]
repo      = os.environ["GITHUB_REPOSITORY"]
pr_number = os.environ.get("PR_NUMBER")

client = OpenAI()  # reads OPENAI_API_KEY from the environment automatically

def get_ai_fix(check_id, resource, file_path, guideline):
    prompt = (
        f"Checkov check {check_id} failed on resource '{resource}' in {file_path}.\n"
        f"Guideline: {guideline}\n\n"
        "Give a concise Terraform HCL fix for AWS. Format:\n"
        "**Issue:** <one line>\n**Fix:**\n```hcl\n<corrected block>\n```\n"
        "**Why this matters:** <one sentence>"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a DevSecOps engineer specializing in Terraform and AWS security. Be concise."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.1,
            timeout=30,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"OpenAI error for {check_id}: {e}")
        return None


def post_pr_comment(body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}
    r = requests.post(url, headers=headers, json={"body": body}, timeout=15)
    print("PR comment posted." if r.status_code == 201 else f"Comment failed: {r.status_code} {r.text}")


def load_findings(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not read {path}: {e}")
        return []
    reports = data if isinstance(data, list) else [data]
    seen, unique = set(), []
    for report in reports:
        for check in report.get("results", {}).get("failed_checks", []):
            cid = check.get("check_id")
            if cid and cid not in seen:
                seen.add(cid)
                unique.append(check)
    return unique


def main():
    if not pr_number:
        print("No PR number, skipping.")
        return
    findings = load_findings("results.json")
    if not findings:
        print("No findings.")
        return

    parts = ["## 🛡️ AI Security Remediation\n",
             f"Checkov found **{len(findings)}** unique issue(s).\n\n---\n"]
    for i, check in enumerate(findings[:5]):
        cid = check.get("check_id", "UNKNOWN")
        res = check.get("resource", "unknown")
        fp  = check.get("file_path", "unknown")
        fix = get_ai_fix(cid, res, fp, check.get("guideline") or cid)
        if fix:
            parts += [f"### Finding {i+1}: `{cid}`\n",
                      f"**Resource:** `{res}` in `{fp}`\n\n", fix + "\n\n---\n"]
        time.sleep(1)
    if len(findings) > 5:
        parts.append(f"_...and {len(findings) - 5} more._\n")
    post_pr_comment("".join(parts))


if __name__ == "__main__":
    main()