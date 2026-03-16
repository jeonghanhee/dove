#!/bin/bash

set -e

echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

OS="$(uname)"

if [[ "$OS" == "Darwin" ]]; then
    echo "Installing macOS dependencies..."

    TMP_DIR=$(mktemp -d)
    cd "$TMP_DIR"

    # fileicon
    if command -v fileicon >/dev/null 2>&1; then
        echo "fileicon already installed"
    else
        if command -v brew >/dev/null 2>&1; then
            echo "Installing fileicon via brew..."
            brew install fileicon
        else
            echo "Installing fileicon from source..."
            git clone https://github.com/mklement0/fileicon.git
            cd fileicon
            make
            mkdir -p ~/bin
            mv fileicon ~/bin/
            chmod +x ~/bin/fileicon
            cd ..
        fi
    fi

    # terminal-notifier
    if command -v terminal-notifier >/dev/null 2>&1; then
        echo "terminal-notifier already installed"
    else
        if command -v brew >/dev/null 2>&1; then
            echo "Installing terminal-notifier via brew..."
            brew install terminal-notifier
        else
            echo "Installing terminal-notifier from source..."
            git clone https://github.com/julienXX/terminal-notifier.git
            cd terminal-notifier
            xcodebuild
            mkdir -p ~/bin
            cp build/Release/terminal-notifier ~/bin/
            chmod +x ~/bin/terminal-notifier
            cd ..
        fi
    fi

    echo "Cleaning up..."
    rm -rf "$TMP_DIR"
fi

echo "Installation complete!"