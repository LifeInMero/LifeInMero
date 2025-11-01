from github import Github, Auth
import os

token = os.getenv("MEROBOT_TOKEN")
if not token:
    raise ValueError("GitHub token not found. Please set MEROBOT_TOKEN in your secrets.")


g = Github(auth=Auth.Token(token))

username = "Meronave"
user = g.get_user(username)

readme_path = "README.md"

emoji_images = {
    "ForkEvent": '<img src="assets/icon.png" width="32" height="32" />',
    "PushEvent": '<img src="assets/icon.png" width="32" height="32" />',
    "IssuesEvent": '<img src="assets/icon.png" width="32" height="32" />'
}

events = user.get_events()[:20]

lines = []
for event in events:
    date = event.created_at.strftime("%m/%d %H:%M")

    if event.type == "ForkEvent":
        img = emoji_images["ForkEvent"]
        action = f"Forked {event.repo.name} to {event.payload['forkee']['full_name']}"
        lines.append(f"[{date}] {img} {action}")

    elif event.type == "PushEvent":
        img = emoji_images["PushEvent"]
        commits = event.payload['commits']
        for commit in commits:
            message = commit['message'].split("\n")[0] 
            lines.append(f"[{date}] {img} {message} {event.repo.name}")

    elif event.type == "IssuesEvent" and event.payload['action'] == 'opened':
        img = emoji_images["IssuesEvent"]
        issue_title = event.payload['issue']['title']
        lines.append(f"[{date}] {img} Issue opened: {issue_title} {event.repo.name}")

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!--START_ACTIVITY-->"
end_tag = "<!--END_ACTIVITY-->"
before = content.split(start_tag)[0] + start_tag + "\n"
after = "\n" + end_tag + content.split(end_tag)[1]

new_content = before + "\n".join(lines) + after

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)
