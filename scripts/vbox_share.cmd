CALL "c:\program files\oracle\virtualbox\vboxmanage" sharedfolder remove %DOCKER_MACHINE_NAME% -name Users
CALL "c:\program files\oracle\virtualbox\vboxmanage" sharedfolder add %DOCKER_MACHINE_NAME% -name Users -hostpath %HOST_SHARE_FOLDER% --automount
CALL "c:\program files\oracle\virtualbox\vboxmanage" setextradata %DOCKER_MACHINE_NAME% VBoxInternal2/SharedFoldersEnableSymlinksCreate/Users 1