set mouse=a
set nocompatible
set backspace=indent,eol,start
set number
set relativenumber
set cursorline
set scrolloff=6
set tabstop=4
set shiftwidth=4
set expandtab

nnoremap <silent> <A-Up> :m .-2<CR>==
nnoremap <silent> <A-Down> :m .+1<CR>==
inoremap <silent> <A-Up> <Esc>:m .-2<CR>==gi
inoremap <silent> <A-Down> <Esc>:m .+1<CR>==gi
vnoremap <silent> <A-Up> :m '<-2<CR>gv=gv
vnoremap <silent> <A-Down> :m '>+1<CR>gv=gv

