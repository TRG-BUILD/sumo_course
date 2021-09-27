# Prerequisites for the SUMO course

Microsimulation part of the _Trafikteknik_ course relies of a couple of prerequisite computer skills and programs. Contact msam@build.aau.dk if you tried but didnt succeed with any of the points below, and you dont know why.



## 1. Command prompt / terminal [](#){name=terminal}
Make sure you have some basic understanding of the Windows command prompt or macOS terminal as it will be used throughout the course. If you are not sure what command prompt and terminal are you can find a good introduction for your OS here:

- [Windows](https://www.youtube.com/watch?v=MBBWVgE0ewk)
- [macOS](https://www.youtube.com/watch?v=aKRYQsKR46I&ab_channel=PercyGrunwaldfromTopTechSkills)
 
## 2. XML file format
Most of SUMO intput and output are organized into eXtensible markdown language (XML) files. Familiarize yourself with the format using [this quick read](https://www.w3schools.com/xml/xml_whatis.asp).

## 3. Text editor
Throughout the course we will be working a lot with a text editor that will let us create and update XML files to simulate different road networkds / traffic demands in sumo. You are free to use your favourite text editor, it can be a NotePad / NotePad++ on Windows, TextEdit on macOS.

If you dont have a preference i recommend [VSCode](https://code.visualstudio.com/) since it is lightweight and supports syntax highlighting for all computer languages / formats and will mark syntax errors for you. VSCode also includes a terminal. Additionally, when we will automate SUMO we can use VSCode to view and write some python code. All in all, from preparing / organizing files, to simulation and automation all can be done from one text editor.

## 4. SUMO installation
Now to the main tool of the lectures. Original SUMO has an OK guidance for installation of the simulator for Windows, macOS and Linux, here we are going to mention some tips to resolve installation problems and verify your installation. Depending on you operation system follow the [original installation page](https://sumo.dlr.de/docs/Downloads.php) and try to install SUMO.

## 5. Verify your installation
If everything went smoothly in point 4 we need to verify that we actually got SUMO on our machine. If you used command prompt (Windows) or terminal (macOS) in the previous step to install SUMO please reset it by closing and opening it again in order to allow a new [environmental varable](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7) called `SUMO_HOME` to be registered. This variable defines a path to the folder on your machine where all SUMO program executable files and helper tools are, without it you would always need to specify where your SUMO tools are explicitly.

After you have restarted the command prompt / terminal type follwing to verify that the environmental variable exists:

__On Windows:__
```sh
echo %SUMO_HOME%
```
__On macOS__:
```sh
echo $SUMO_HOME
```

Should output a path to where sumo is installed SUMO for example:

```sh
C:\ProgramFIles (x86)\Eclipse\Sumo\
```

Another test is to see whether SUMO can be called from the command window / terminal:
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

If you didnt get errors up to this point the SUMO is set up correctly.
### Possible problems
#### Windows
Obtaining `.msi` file from the website and running it with a double click might result in a bug where installation does not start because "another installation is already running". To resolve this issue you will install SUMO using command prompt. [Open the command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/) with your favourite method, using CTRL + R or searching for command prompt. Locate the folder with downloaded `.msi` file using `cd` (change directory) command. Get to know your basics from [this guide](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) if you are new to operating command line. Use the command `msiexec.exe -i [your file name]` to start the installation. [Msiexec](https://www.advancedinstaller.com/user-guide/msiexec.html) is a command that is being called when you double click on a `.msi` file. On our lab PC the entire procedure looks something like this:

```sh
cd C:\Users\TRG\Downloads
msiexec.exe -i sumo-win64-1.7.0.msi
```

Verify your installation as described in the previous section.

## 6. Python
