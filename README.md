# Activity Browser Launcher
Don't want to deal with manually installing Conda, the Activity Browser packages, and keeping them all up to date? Use the Activity Browser launcher that manages this for you instead. Download the newest installer for your operating system from the releases page.

**This software is still in its alpha stage: use at your own risk**

_Supported on Windows and MacOS_

## Building the launcher yourself

- Install (Mini)Conda
- Create the build environment using the right .yml in the `.github/environments` folder
- Build for your OS by either using `pyinstaller windows.spec` or `pyinstaller macos.spec`
- Enjoy the fruits of your labour that may be found in the newly created `dist` folder