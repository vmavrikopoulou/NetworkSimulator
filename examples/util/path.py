import sys
from pathlib import Path

# this is used for profiling
basePath = sys.path[0]
if sys.path[0] == '':
    basePath = "/Users/alex/Dropbox/DoBots/Projects/Python/NetworkSimulator/examples"
    
    
# Because python searches for local imports in the sys.path folders, we need to add the root folder of this project to
# the sys.path. Since this path.py will be called from the folder /<projectRoot>/examples, we need to go one dir up to
# get the project root.

parentsOfScriptFolder = Path(basePath).parents

# add the stringified parent folder to the sys.path so our imports can be evaluated.
sys.path.append(str(parentsOfScriptFolder[0]))
