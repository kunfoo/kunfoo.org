# Bash
## Arrays
create an array in variable FOO
```
FOO=(foo bar baz)
```
access element 1 of FOO
```
${FOO[1]}
```
give us all elements of FOO
```
${FOO[@]}
```
give us the number of elements FOO contains
```
${#FOO[@]}
```

## Environment Variables
- HISTFILE
    - set path to file, where bash history is stored (default ~/.bash\_history)
    - f.e. disable history: `HISTFILE=/dev/null`
- LC\_ALL
    - override all localisation settings
    - f.e. read manpage in system's/application's 'default' language: `LC_ALL=C man man`
- TMOUT
    - session timeout in seconds
    - f.e. kill the shell after 5 minutes of inactivity: `TMOUT=300`

## misc
use vi-keybindings in bash
```
set -o vi
```
