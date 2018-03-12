from github import Github
import subprocess
import logging
import time

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# log into github
g = Github(login_or_token='<insert creds>',
           password=None,
           base_url="https://api.github.com")
# specify the repo you want to watch
repo_name = 'blockchain-example'
branch_to_monitor = 'master'

while True:
    repo = g.get_user().get_repo(repo_name)
    last_commit_sha = repo.get_branch(branch_to_monitor).commit.sha
    logger.info('Latest sha: ' + last_commit_sha)
    last_files_changed = repo.get_commit(last_commit_sha).files

    def retrieve_files_changed(last_files_changed):
        """ Retrieved the files changed from a sha """
        changed_files = [file.filename for file in last_files_changed]
        return changed_files

    def is_ci_needed(changed_files):
        """ Check if we need to run CI """
        for file in changed_files:
            if file.startswith('.coverage'):
                logger.info('no changes necessary')
            else:
                logger.info('Need to re-run our test suite')
                return True
        return False

    changed_files = retrieve_files_changed(last_files_changed)

    if is_ci_needed(changed_files) == True:
        try:
            logger.info(subprocess.check_output(
                ['git', 'checkout', last_commit_sha, '-b' 'testing-suite']))
            logger.info(subprocess.check_output(['pytest', '--cov=.', '.']))
            logger.info(subprocess.check_output(
                ['git', 'checkout', branch_to_monitor]))
            logger.info(subprocess.check_output(['git', 'add', '.coverage']))
            logger.info(subprocess.check_output(
                ['git', 'commit', '-m', '"updating tests"']))
            logger.info(subprocess.check_output(
                ['git', 'push', 'origin', branch_to_monitor]))
            logger.info(subprocess.check_output(
                ['git', 'branch', '-D', 'testing-suite']))
        except Exception as e:
            logger.critical(
                'Tests failed. Will re-run in 60 seconds to see if they are fixed')
            exit()
    # wait 60 seconds before checking again
    time.sleep(60)
