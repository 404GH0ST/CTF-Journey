git log -p | grep -oP "\+[a-zA-Z-0-9{}_]$" | tr -d "+" | tr -d "
" | rev
