# CG
CG Project

To contribute: 

- git checkout master
- git fetch origin
- git merge origin/master
- git checkout -b new-feature

do changes

- git add, git commit
- git checkout master
- git fetch origin
- git merge origin/master
- git checkout new-feature
- git rebase master
- git checkout master
- git merge new-feature
- git push origin master

To run it:
cd <project-folder>
source env/bin/activate
MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 python main.py
