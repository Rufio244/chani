from github_connector import ChaniGitHub


chani = ChaniGitHub()


system_files = [

{
"path":"README.md",
"content":
"""
# Chani AI Core

Auto deployed system.
"""
},

{
"path":"core.py",
"content":
"""
class Chani:

    def think(self,data):
        return "processing "+str(data)
"""
}

]


result = chani.push_system(system_files)

print(result)
