# SUMO installation
Original SUMO has an OK guidance for installation of the simulator, here we are going to mention some tips to resolve installation problems and verify your installation. 

Depending on you operation system follow the [original installation page](https://sumo.dlr.de/docs/Downloads.php) and try to install SUMO.

# Windows
Make sure you have some basic understanding of the Windows command prompt. You can find a good introduction [here](https://www.youtube.com/watch?v=MBBWVgE0ewk).

## Verify your installation
If you used previous step to install SUMO please restart the command prompt (close and open new) in order to allow new [environmental varable](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7) called `SUMO_HOME`. This variable defines a path to the folder where all SUMO program executable files are, without it you would always need to specify where your SUMO tools are.

After you have restarted the command prompt type follwing to verify your installation:

```sh
echo %SUMO_HOME%
```

Should output a path to where sumo is installed SUMO:

```sh
C:\ProgramFIles (x86)\Eclipse\Sumo\
```

Another test is to type:
```sh
sumo --version
```

Depending on your version should output something like that:

```
Eclipse SUMO sumo Version 1.7.0
 Build features: Windows-6.3.9600 AMD64 MSVC 18.0.40629.0 Release Proj GUI SWIG
 Copyright (C) 2001-2020 German Aerospace Center (DLR) and others; https://sumo.dlr.de

Eclipse SUMO sumo Version 1.7.0 is part of SUMO.
This program and the accompanying materials
are made available under the terms of the Eclipse Public License v2.0
which accompanies this distribution, and is available at
http://www.eclipse.org/legal/epl-v20.html
SPDX-License-Identifier: EPL-2.0
```

## Possible problems
Obtaining `.msi` file from the website and running it with a double click might result in a bug where installation does not start because "another installation is already running". To resolve this issue you will install SUMO using command prompt. [Open the command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) with your favourite method, using CTRL + R or searching for command prompt. Locate the folder with downloaded `.msi` file using `cd` (change directory) command. Get to know your basics from [this guide](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) if you are new to operating command line. Use the command `msiexec.exe -i [your file name]` to start the installation. [Msiexec](https://www.advancedinstaller.com/user-guide/msiexec.html) is a command that is being called when you double click on a `.msi` file. On our lab PC the entire procedure looks something like this:

```sh
cd C:\Users\TRG\Downloads
msiexec.exe -i sumo-win64-1.7.0.msi
```

Verify your installation as described in the previous section.