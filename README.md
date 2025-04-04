## DummyKeybinds

A simple plugin for JetBrains IDEs that adds a new base keymap with no shortcuts assigned. This allows you to have your own keymap inherit zero other shortcuts from a parent.  
This is useless if you don't care about your keymap depending on another one.

### Usage
Install the plugin by going to Settings -> Plugins -> Gear Icon -> Install from disk. Prebuilts are available in Github Releases.

### Making an independent keymap
To make a keymap that combines all bindings from its parent, making one XML representing the IDE's effective keymap, modify and run the merge-keymaps.py script.