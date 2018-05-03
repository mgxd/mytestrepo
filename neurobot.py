mport re
import logging

logger = logging.getLogger()

class RepoHelper(object):

    def __init__(self, gh, repoID):
        """
        Initialize Repository Helper object

        Parameters
        ----------
        gh : github.Github
            Github log in
        repoID : int
            ID of repo
        """
        self._gh = gh
        self._repoID = repoID
        self.repo = self._gh.get_repo(self._repoID)


    @property
    def labels(self):
        """Return most recent labels"""
        return [lbl for lbl in self.repo.get_labels()]


    @property
    def issues(self):
        """Return most recent issues"""
        return [iss for iss in self.repo.get_issues()]


    @property
    def milestones(self):
        """Return most recent milestones"""
        return [ms for ms in self.repo.get_milestones()]


    @property
    def pulls(self):
        return [pr for pr in self.repo.get_pulls()]


    def _fetch_latest_milestone(self):
        """Fetch latest open milestone in repo"""
        if self.milestones:
            for ms in self.milestones:
                if ms.state == 'open':
                    return pull


    def _fetch_latest_issue(self):
        """Fetch top issue, fails if no issues are present"""
        if self.issues:
            return self.repo.get_issues()[0]


    def _fetch_latest_pull(self):
        """Fetch top pull request in repo"""
        if self.pulls:
            return self.repo.get_pulls()[0]


    # TODO: generalize across issues/milestones
    def apply_label(self, applyee=None):
        """Fetches latest issue and applies first existing label that matches"""
        issue = self._fetch_latest_issue()
        match = re.search(r'(?<=### Label\r\n)\w+', issue.body)
        if not match:
            # template missing so let's skip
            logger.warning('Issue template not detected.')
            return
        label = match.group().lower()
        # search if label exists
        rlabels = [lbl for lbl in self.labels if lbl.name in label]
        if rlabels:
            print("Applying labels")
            iss.set_labels(rlabels[0])
        else:
            # let's ignore instead of making for now
            pass


    def fetch_milestone(self):
        """Fetch current milestone"""
        ms = self.repo._fetch_latest_milestone()
        if not ms.state == 'open':
            # milestone is completed or closed
            raise RuntimeError("Latest milestone is closed.")
