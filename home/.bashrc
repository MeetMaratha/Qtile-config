#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

# Custom theme ---------------------------
# Synth Shell
#if [ -f /home/meet/.config/synth-shell/synth-shell-prompt.sh ] && [ -n "$(echo $- | grep i)" ]; then
#	source /home/meet/.config/synth-shell/synth-shell-prompt.sh
#fi
#eval "$(starship init bash)"
exec fish
