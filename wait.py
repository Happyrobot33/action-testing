from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
workflow_run_id = int(os.getenv("WORKFLOW_RUN_ID"))

auth = Auth.Token(github_token)
g = Github(auth=auth)
repo = g.get_repo(repo_name)
print(f"Authenticated to repo {repo.full_name}")

#now find the workflow run list for the que workflow, and see if there is any before us
workflows_running = repo.get_workflow_runs(status="in_progress")
#also get any qued
workflows_queued = repo.get_workflow_runs(status="queued")
all_workflows = workflows_running + workflows_queued

#loop and get all their IDs, and check if ANY are less than us
ids = [w.id for w in all_workflows]
print(f"Found {len(ids)} queued or running workflow runs: {ids}")
while any(wid < workflow_run_id for wid in ids):
    print("There are still workflow runs queued or running before us, waiting 10 seconds...")
    time.sleep(10)
    workflows_running = repo.get_workflow_runs(status="in_progress")
    workflows_queued = repo.get_workflow_runs(status="queued")
    all_workflows = workflows_running + workflows_queued
    ids = [w.id for w in all_workflows]
    print(f"Found {len(ids)} queued or running workflow runs: {ids}")
