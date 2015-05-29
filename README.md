# CG
CG Project

To contribute: 

Get latest changes:
- git checkout master
- git fetch origin
- git merge origin/master

Create new working branch:
- git checkout -b new-feature

do changes

Stage your changes and write the history:
- git add, git commit

Re-update master before pushing:
- git checkout master
- git fetch origin
- git merge origin/master
 
Update your branch:
- git checkout new-feature
- git rebase master
 
Update master with your branch:
- git checkout master
- git merge new-feature

Push changes to Github:
- git push origin master

To run it:
- cd < project-folder >
- source < env-name >/bin/activate
- MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 python main.py

First time you need to add:
- cd < project-folder >
- virtualenv < env-name >
- source <env-name>/bin/activate
- pip install -r requirements.txt
