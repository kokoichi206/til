#!/bin/bash -

function OS_NAME()
{
    if type -t wevtutil &> /dev/null
    then
        OS=MSWin
    elif type -t scutil &> /dev/null
    then
        OS=macOS
    else
        OS=Linux
    fi
    # returnは終了ステータスを返すだけ！
}
OS_NAME
echo $OS
