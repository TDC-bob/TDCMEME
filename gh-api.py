# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard. If not, see <http://www.gnu.org/licenses/>.

try:
    import json
except ImportError:
    from lib import simplejson as json

import urllib.request as urllib
##from urllib import

class GitHub(object):
    """
Simple api wrapper for the Github API v3. Currently only supports the small thing that SB
needs it for - list of cimmots.
"""

    def _access_API(self, path, params=None):
        """
Access the API at the path given and with the optional params given.
path: A list of the path elements to use (eg. ['repos', 'midgetspy', 'Sick-Beard', 'commits'])
params: Optional dict of name/value pairs for extra params to send. (eg. {'per_page': 10})
Returns a deserialized json object of the result. Doesn't do any error checking (hope it works).
"""

        url = 'https://api.github.com/' + '/'.join(path)

        if params and type(params) is dict:
            url += '?' + '&'.join([str(x) + '=' + str(params[x]) for x in params.keys()])

        return json.load(urllib.urlopen(url))

    def commits(self, user, repo, branch='master'):
        """
Uses the API to get a list of the 100 most recent commits from the specified user/repo/branch, starting from HEAD.
user: The github username of the person whose repo you're querying
repo: The repo name to query
branch: Optional, the branch name to show commits from
Returns a deserialized json object containing the commit info. See http://developer.github.com/v3/repos/commits/
"""
        return self._access_API(['repos', user, repo, 'commits'], {'per_page': 100, 'sha': branch})

class UpdateManager():
    def get_update_url(self):
        return sickbeard.WEB_ROOT+"/home/update/?pid="+str(sickbeard.PID)

class GitUpdateManager(UpdateManager):

    def __init__(self):
        self._cur_commit_hash = None
        self._newest_commit_hash = None
        self._num_commits_behind = 0

        self.git_url = 'http://code.google.com/p/sickbeard/downloads/list'

        self.branch = self._find_git_branch()

    def _git_error(self):
        error_message = 'Unable to find your git executable - either delete your .git folder and run from source OR <a href="http://code.google.com/p/sickbeard/wiki/AdvancedSettings" onclick="window.open(this.href); return false;">set git_path in your config.ini</a> to enable updates.'
        sickbeard.NEWEST_VERSION_STRING = error_message

        return None

    def _run_git(self, args):

        if sickbeard.GIT_PATH:
            git_locations = ['"'+sickbeard.GIT_PATH+'"']
        else:
            git_locations = ['git']

        # osx people who start SB from launchd have a broken path, so try a hail-mary attempt for them
        if platform.system().lower() == 'darwin':
            git_locations.append('/usr/local/git/bin/git')

        output = err = None

        for cur_git in git_locations:

            cmd = cur_git+' '+args

            try:
                logger.log(u"Executing "+cmd+" with your shell in "+sickbeard.PROG_DIR, logger.DEBUG)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=sickbeard.PROG_DIR)
                output, err = p.communicate()
                logger.log(u"git output: "+output, logger.DEBUG)
            except OSError:
                logger.log(u"Command "+cmd+" didn't work, couldn't find git.")
                continue

            if p.returncode != 0 or 'not found' in output or "not recognized as an internal or external command" in output:
                logger.log(u"Unable to find git with command "+cmd, logger.DEBUG)
                output = None
            elif 'fatal:' in output or err:
                logger.log(u"Git returned bad info, are you sure this is a git installation?", logger.ERROR)
                output = None
            elif output:
                break

        return (output, err)


    def _find_installed_version(self):
        """
Attempts to find the currently installed version of Sick Beard.

Uses git show to get commit version.

Returns: True for success or False for failure
"""

        output, err = self._run_git('rev-parse HEAD') #@UnusedVariable

        if not output:
            return self._git_error()

        logger.log(u"Git output: "+str(output), logger.DEBUG)
        cur_commit_hash = output.strip()

        if not re.match('^[a-z0-9]+$', cur_commit_hash):
            logger.log(u"Output doesn't look like a hash, not using it", logger.ERROR)
            return self._git_error()

        self._cur_commit_hash = cur_commit_hash

        return True

    def _find_git_branch(self):

        branch_info = self._run_git('symbolic-ref -q HEAD')

        if not branch_info or not branch_info[0]:
            return 'master'

        branch = branch_info[0].strip().replace('refs/heads/', '', 1)

        return branch or 'master'


    def _check_github_for_update(self):
        """
Uses pygithub to ask github if there is a newer version that the provided
commit hash. If there is a newer version it sets Sick Beard's version text.

commit_hash: hash that we're checking against
"""

        self._num_commits_behind = 0
        self._newest_commit_hash = None

        gh = github.GitHub()

        # find newest commit
        for curCommit in gh.commits('midgetspy', 'Sick-Beard', self.branch):
            if not self._newest_commit_hash:
                self._newest_commit_hash = curCommit['sha']
                if not self._cur_commit_hash:
                    break

            if curCommit['sha'] == self._cur_commit_hash:
                break

            self._num_commits_behind += 1

        logger.log(u"newest: "+str(self._newest_commit_hash)+" and current: "+str(self._cur_commit_hash)+" and num_commits: "+str(self._num_commits_behind), logger.DEBUG)

    def set_newest_text(self):

        # if we're up to date then don't set this
        if self._num_commits_behind == 100:
            message = "or else you're ahead of master"

        elif self._num_commits_behind > 0:
            message = "you're %d commit" % self._num_commits_behind
            if self._num_commits_behind > 1: message += 's'
            message += ' behind'

        else:
            return

        if self._newest_commit_hash:
            url = 'http://github.com/midgetspy/Sick-Beard/compare/'+self._cur_commit_hash+'...'+self._newest_commit_hash
        else:
            url = 'http://github.com/midgetspy/Sick-Beard/commits/'

        new_str = 'There is a <a href="'+url+'" onclick="window.open(this.href); return false;">newer version available</a> ('+message+')'
        new_str += "&mdash; <a href=\""+self.get_update_url()+"\">Update Now</a>"

        sickbeard.NEWEST_VERSION_STRING = new_str

    def need_update(self):
        self._find_installed_version()
        try:
            self._check_github_for_update()
        except Exception as e:
            logger.log(u"Unable to contact github, can't check for update: "+repr(e), logger.ERROR)
            return False

        logger.log(u"After checking, cur_commit = "+str(self._cur_commit_hash)+", newest_commit = "+str(self._newest_commit_hash)+", num_commits_behind = "+str(self._num_commits_behind), logger.DEBUG)

        if self._num_commits_behind > 0:
            return True

        return False

    def update(self):
        """
Calls git pull origin <branch> in order to update Sick Beard. Returns a bool depending
on the call's success.
"""

        output, err = self._run_git('pull origin '+self.branch) #@UnusedVariable

        if not output:
            return self._git_error()

        pull_regex = '(\d+) .+,.+(\d+).+\(\+\),.+(\d+) .+\(\-\)'

        (files, insertions, deletions) = (None, None, None)

        for line in output.split('\n'):

            if 'Already up-to-date.' in line:
                logger.log(u"No update available, not updating")
                logger.log(u"Output: "+str(output))
                return False
            elif line.endswith('Aborting.'):
                logger.log(u"Unable to update from git: "+line, logger.ERROR)
                logger.log(u"Output: "+str(output))
                return False

            match = re.search(pull_regex, line)
            if match:
                (files, insertions, deletions) = match.groups()
                break

        if None in (files, insertions, deletions):
            logger.log(u"Didn't find indication of success in output, assuming git pull failed", logger.ERROR)
            logger.log(u"Output: "+str(output))
            return False

        return True

def main():
    test = GitHub()
    pouet = test.commits("TDC-bob","TDCMEME")
    print(pouet)

if __name__ == '__main__':
    main()