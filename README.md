# Ecommerce

Goal: Develop an ecommerce website.

## Instructions to set up the development environment and run the project locally on Linux

1. Install [Git](https://git-scm.com/download/linux)

    ```sh
    sudo add-apt-repository ppa:git-core/ppa
    sudo apt update && sudo apt upgrade -y
    git --version
    git config --global user.name "<username>"
    git config --global user.email "<email>"
    git config --global init.defaultBranch main
    ```

2. Install [Zsh](https://github.com/ohmyzsh/ohmyzsh/wiki)

    ```sh
    sudo apt install zsh
    wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
    sh install.sh
    sudo git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    sudo git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

    # https://github.com/kaplanelad/shellfirm#installation
    sudo curl https://raw.githubusercontent.com/kaplanelad/shellfirm/main/shell-plugins/shellfirm.plugin.zsh --create-dirs -o ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/shellfirm/shellfirm.plugin.zsh

    nano ~/.zshrc

    plugins=(zsh-autosuggestions zsh-syntax-highlighting shellfirm)

    exec "$SHELL"
    ```

3. Install [VS Code](https://code.visualstudio.com/download)

4. Install the latest Python version using [pyenv](https://github.com/pyenv/pyenv).

    ```sh
    sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    curl https://pyenv.run | bash

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc

    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc

    echo 'eval "$(pyenv init -)"' >> ~/.zshrc

    pyenv versions

    pyenv install 3.10.7

    pyenv global 3.10.7
    ```

5. Install the Python package manager, [Poetry](https://python-poetry.org/docs/).

    ```sh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

    curl -sSL https://install.python-poetry.org | python3 -

    poetry -V

    poetry self update

    poetry config virtualenvs.in-project true

    poetry new <project-name>

    cd <project-name>
    # Activate environment
    poetry shell
    # Install packages from requirements.txt
    cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add
    poetry update
    poetry export --without-hashes > requirements.txt
    ```

6. Start server

    `./manage.py runserver`

7. Run tests

    `./manage.py test`
