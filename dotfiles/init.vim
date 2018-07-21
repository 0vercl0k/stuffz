" Axel '0vercl0k' Souchet - 6-July-2018

call plug#begin()
Plug 'scrooloose/nerdtree'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'lifepillar/vim-solarized8'
Plug 'yggdroot/indentline'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
call plug#end()

" Bugz
"" nvim 0.3 bug workaround - see https://github.com/equalsraf/neovim-qt/issues/417
if @% == ''
  bd
endif

" General
"" Be friendly to Windows. pls.
source $VIMRUNTIME/mswin.vim
"" Allow to select text with the mouse
set mouse=a
"" Line numbers on the left side
set number
"" tab -> 4spaces
set tabstop=4 shiftwidth=4 expandtab
"" Solarized theme
set background=dark
colorscheme solarized8
"" py2 annaconda
let g:python_host_prog = 'C:/ProgramData/Anaconda2/python.exe'

" Plugins
"" NERDTree
""" Show bookmarks
let NERDTreeShowBookmarks = 1
""" Update CWD (useful to have CtrlP working)
let NERDTreeChDirMode = 2
""" Open a tree on open
autocmd vimenter * NERDTree
""" Close neovim if the only left window opened is a NERDTree
autocmd bufenter * if (winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree()) | q | endif

"" CtrlP
""" Disable the project root finding heuristics
let g:ctrlp_working_path_mode = ''

"" indentline
""" Show leading spaces
let g:indentLine_leadingSpaceEnabled = 1
""" Uses the character '.' as leading space character
let g:indentLine_leadingSpaceChar = '.'
""" Uses the character '.' as indent character
let g:indentLine_char = '.'

"" vim-airline
""" Enable the buffers showing up at the top of the screen
let g:airline#extensions#tabline#enabled = 1

"" vim-airline-themes
""" Solarized dark theme for vim-airline
let g:airline_solarized_bg = 'dark'
