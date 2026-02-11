# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
# ZSH_THEME="robbyrussell"
# ZSH_THEME="clean"
ZSH_THEME="powerlevel10k/powerlevel10k"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

DISABLE_AUTO_UPDATE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git zsh-autosuggestions zsh-syntax-highlighting conda)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

alias py="python3.12"
alias nv="watch -n 1 -d nvidia-smi"
alias dotfilesc="code ~/.dotfiles"
alias tokensc="code ~/Code/github.tokens"
alias tokens="cat ~/Code/github.tokens"
alias vps="cd ~/keys"

reset_opencode() {
  PKG="opencode-ai"

  command -v npm >/dev/null || { echo "npm not found"; return 1; }

  echo "▶ Removing $PKG (npm)"
  npm uninstall -g "$PKG" >/dev/null 2>&1 || true

  GLOBAL_ROOT="$(npm root -g)"
  PKG_PATH="$GLOBAL_ROOT/$PKG"

  echo "▶ Force-cleaning leftovers"
  rm -rf "$PKG_PATH"
  find "$GLOBAL_ROOT" -maxdepth 1 -type d -name ".${PKG}-*" -exec rm -rf {} +

  echo "▶ Cleaning npm cache"
  npm cache clean --force >/dev/null 2>&1

  echo "▶ Reinstalling $PKG"
  npm i -g "$PKG" || {
    echo "✖ Install failed"
    return 1
  }

  echo "▶ Verifying"
  if command -v opencode >/dev/null; then
    echo "✔ opencode fixed"
  else
    echo "✖ opencode still missing from PATH"
    echo "Run: nvm use --default"
    return 1
  fi
}


gwork() {
    git config user.name "tmambinge"
    git config user.email "tmambinge@mugonat.com"
}

gpersonal() {
    git config user.name "tanaka-mambinge"
    git config user.email "tmambingez@gmail.com"
}

jp() {
    if [ -z "$1" ]; then
        echo "Please select a conda environment:"
        conda env list
    else
        conda activate "$1"
        jupyter lab --no-browser
    fi
}

cenv() {
    if [ -z "$1" ]; then
        echo "Please select a conda environment:"
        conda env list
    else
        conda activate "$1"
    fi
}

venv() {
    if [ -z "$1" ]; then
        if [ -d "./env" ]; then
            source ./env/bin/activate
        else
            echo "No environment found in ./env"
            return 1
        fi
    else
        if [ -d "$1/env" ]; then
            source "$1/env/bin/activate"
        else
            echo "No environment found in $1/env"
            return 1
        fi
    fi
}

android() {
    local emulator
    emulator=$(emulator -list-avds | fzf --height 40% --reverse --border --prompt="Select an emulator: ")
    if [ -n "$emulator" ]; then
        emulator -avd "$emulator"
    else
        echo "No emulator selected."
        return 1
    fi
}

workspaces() {
  local DIR="$HOME/.local/share/warp-terminal/launch_configurations"

  [[ -d "$DIR" ]] || {
    echo "Warp launch config directory not found: $DIR"
    return 1
  }

  local file
  file=$(ls -1 "$DIR" | fzf --prompt="Warp config > ")

  [[ -n "$file" ]] || return 0

  code "$DIR/$file"
}

devsvc() {
  # label|systemd_unit
  local services=(
    "PostgreSQL (postgresql-17)|postgresql-17"
    "MySQL (mysqld)|mysqld"
    "MongoDB (mongod)|mongod"
    "Typesense (typesense-server)|typesense-server"
    "Valkey (valkey)|valkey"
    "OpenCode (opencode) [user]|--user opencode"
  )

  command -v fzf >/dev/null 2>&1 || {
    echo "fzf not found. Install with: sudo dnf install fzf"
    return 1
  }

  local choice unit action
  choice=$(printf "%s\n" "${services[@]}" | fzf --prompt="Service > " --height=40% --reverse)

  [[ -n "$choice" ]] || return 0

  unit="${choice##*|}"

  action=$(printf "%s\n" start stop restart status | fzf --prompt="Action > " --height=20% --reverse)
  [[ -n "$action" ]] || return 0

  # Check if it's a user service
  local user_flag=""
  if [[ "$unit" == --user* ]]; then
    user_flag="--user"
    unit="${unit#--user }"
  fi

  case "$action" in
    start|stop|restart) systemctl $user_flag "$action" "$unit" ;;
    status) systemctl $user_flag status "$unit" --no-pager ;;
    *) return 0 ;;
  esac
}



# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# android studio
export ANDROID_SDK_ROOT="$HOME/Android/Sdk"
export ANDROID_HOME="$ANDROID_SDK_ROOT"
export PATH="$PATH:$ANDROID_HOME/emulator"
export PATH="$PATH:$ANDROID_HOME/platform-tools"
export PATH="$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin"

# flutter
export PATH="$PATH:/home/tanaka/flutter/bin"

# mongo
export PATH="$PATH:/usr/bin/mongod"


export PATH="/usr/local/cuda-12.9/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH"

# warp
export WGPU_BACKEND=gl

# sqlite utils shell completions
export PATH="$HOME/.local/bin:$PATH"
eval "$(_SQLITE_UTILS_COMPLETE=zsh_source sqlite-utils)"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/tanaka/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/tanaka/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/tanaka/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/tanaka/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# devtunnels
export PATH="$HOME/.local/bin:$PATH"
export PATH="/home/tanaka/.config/herd-lite/bin:$PATH"
export PHP_INI_SCAN_DIR="/home/tanaka/.config/herd-lite/bin:$PHP_INI_SCAN_DIR"

# bun completions
[ -s "/home/t12e/.bun/_bun" ] && source "/home/t12e/.bun/_bun"

# bun
export PATH="$HOME/.bun/bin:$PATH"

# eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
export PATH="$HOME/.nvm/versions/node/$(nvm version default)/bin:$PATH"
