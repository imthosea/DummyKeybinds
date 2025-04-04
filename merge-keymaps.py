"""
This script merges a parent and child keymap XML and makes
an independent keymap XML that represents what keymap actually takes effect in the IDE.
To get a fully independent keymap, you will probably need to run it multiple times,
going through the inheritance chain.
Most keymaps depend on "default", so as an example you would run:
Run #1. Parent: Default / Child: Eclipse Keymap
Run #2. Parent: Result of run #1 / Child: Your keymap
The result of that would be identical to what is effective in the IDE, all in one XML.

Default and built-in keymaps:
https://github.com/JetBrains/intellij-community/tree/master/platform/platform-resources/src/keymaps
Permalink if its moved: https://github.com/JetBrains/intellij-community/tree/8fc29e4001db7ecb3680d839b52a7b31bc687bce/platform/platform-resources/src/keymaps
For ones in the marketplace, download the file from the web
(i.e. https://plugins.jetbrains.com/plugin/12559-eclipse-keymap/versions/stable)
extract the jar from the lib directory in the zip, then extract the keymap folder from the jar.

This requires spaces for indentation in the XMLs, and assumes no blank lines at the top or bottom.
Totally unoptimized, but gets the job done.
"""

import re

# Constants
parent_path = "<PATH-TO-PARENT>"
# anything in the child XML overrides the parent
child_path = "<PATH-TO-CHILD>"
output_path = "<PATH-TO-OUTPUT>"
output_keymap_header='<keymap version="1" name="<KEYMAP-NAME>" parent="DummyKeybinds">'

def get_id(line):
    match = re.search(r'<action id="([^"]+)"', line)
    return match.group(1) if match else None

with open(parent_path) as f:
    # don't include header and </keymap>
    parent_lines = f.read().splitlines()[1:-1]

with open(child_path) as f:
    child_lines = f.read().splitlines()[1:-1]
    used_ids = []
    for line in child_lines:
        if line.strip():
            id = get_id(line)
            if id:
                used_ids.append(id)

output_lines = [output_keymap_header]

allow_sub = False
for line in parent_lines:
    if not line.strip():
        continue

    if line.startswith("    "): # keystroke definition
        if allow_sub:
            output_lines.append(line)
        continue
    if line == "  </action>":
        if allow_sub:
            output_lines.append(line)
            allow_sub = False
        continue

    id = get_id(line)
    if id and id not in used_ids:
        output_lines.append(line)
        if not line.endswith("</action>") and not line.endswith("/>"): # ignore one-liners
            allow_sub = True

for line in child_lines:
    if not line.strip():
        continue
    # don't write "overide key to nothing" entries
    # i.e. <action id="CloseEditor"/>
    if line.startswith("    ") or not line.endswith("/>"):
        # any matching key definition will not be written, so we can just append the child after
        output_lines.append(line)

output_lines.append("</keymap>")

with open(output_path, "w") as f:
    f.write("\n".join(output_lines) + "\n")
print(f"Wrote to {output_path}")