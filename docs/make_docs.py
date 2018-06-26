# !/bin/python

import os
import subprocess
import sys
import yaml

def main(argv):
    # Ensure the script always runs from the same location
    dirname = os.path.dirname(argv[0])
    script_dir = os.path.abspath('./{0}'.format(dirname))
    os.chdir(script_dir)

    _params_file = os.path.join(script_dir, 'PARAMS.yml')
    if os.path.exists(_params_file):
        with open(_params_file, 'r') as stream:
            try:
                params = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)
       
    username = params.get('username')
    project_files = params.get('project_files')
    project = params.get('project')
    build_dir  = os.path.abspath('../../tmp_{0}').format(project_files)
    github_dir = '{0}/html'.format(build_dir)

    try:
        os.mkdir(build_dir)
    except OSError as exc:
        print(exc)
        
    yeses = ['y', 'Y', 'Yes', 'yes']
    if os.path.exists(github_dir):
        remove_old = input("gh-pages dir '{0}' already exists, deleting it. [y/n]".format(github_dir))
        if remove_old in yeses:
            subprocess.run(['rm', '-rf', github_dir])

    clone_command = [
        'git',
        'clone',
        'git@github.com:{0}/{1}'.format(username, project),
        '-b',
        'gh-pages',
        github_dir
        ]

    subprocess.run(clone_command)
    subprocess.run(['make', 'html'])
    # Commit/push changes
    commit = input("Commit to gh-pages branch? [y/n]\n")
    if commit in yeses:
        os.chdir(github_dir)
        # if commit msg on command line use that

        # otherwise get it from input
        commit_msg = input("Enter commit message: ")

        subprocess.run(['git', 'add', '-A'])
        subprocess.run(['git', 'commit', '-m', commit_msg])
        push = input("Push to origin? [y/n]\n")
        if push in yeses:
            subprocess.run(['git', 'push'])
        os.chdir(script_dir)


    # Remove build dir
    remove = input("Remove build dir '{0}'? [y/n]\n".format(build_dir))
    if remove in yeses:
        subprocess.run(['rm', '-rf', build_dir])

if __name__=="__main__":
    main(sys.argv)
