from github import Github
import subprocess
import logging
import time

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# log into github

while True:
    repo_name = "blockchain-example"
    repo = g.get_user().get_repo(repo_name)
    last_commit_sha = repo.get_branch("master").commit.sha
    logger.info('Latest sha: ' + last_commit_sha)
    last_files_changed = repo.get_commit(last_commit_sha).files

    def retrieve_files_changed(last_files_changed):
        """ # convert this into a list comprehension """
        changed_files = []
        for file in last_files_changed:
            changed_files.append(file.filename)
        return changed_files

    def is_ci_needed(changed_files):
        for file in changed_files:
            if file.startswith('.coverage'):
                logger.info('no changes necessary')
            else:
                logger.info('need to do CI stuff')
                return True
        return False

    changed_files = retrieve_files_changed(last_files_changed)

    if is_ci_needed(changed_files) == True:
        try:
            logger.info(subprocess.check_output(['pytest', '--cov=.', '.']))
            logger.info(subprocess.check_output(['git', 'add', '.coverage']))
            logger.info(subprocess.check_output(
                ['git', 'commit', '-m', '"updating tests"']))
            logger.info(subprocess.check_output(
                ['git', 'push', 'origin', 'master']))
        except Exception as e:
            logger.critical('Tests failed. See report above')
            exit()
    # wait 60 seconds before checking again
    time.sleep(60)
