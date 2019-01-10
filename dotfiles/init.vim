" Axel '0vercl0k' Souchet - 6-July-2018

call plug#begin()
Plug 'scrooloose/nerdtree'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'lifepillar/vim-solarized8'
Plug 'yggdroot/indentline'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
call plug#end()

" General
"" Be friendly to Windows. pls.
source $VIMRUNTIME/mswin.vim
"" Allow to select text with the mouse
set mouse=a
"" tab -> 4spaces
set tabstop=4 shiftwidth=4 expandtab
"" Solarized theme
set background=dark
colorscheme solarized8
"" py2 annaconda
let g:python_host_prog = 'C:/ProgramData/Anaconda2/python.exe'
"" Hybrid line numbers
set number relativenumber
augroup numbertoggle
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
  autocmd BufLeave,FocusLost,InsertEnter   * set norelativenumber
augroup END

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
""" Show the tab number (not the buffer numbers)
let g:airline#extensions#tabline#show_tab_nr = 1
""" Enable displaying index of the buffers; When enabled,
""" mappings will be exposed to allow you to select a buffer directly
let g:airline#extensions#tabline#buffer_idx_mode = 1
""" Said mappings
nmap <leader>1 <Plug>AirlineSelectTab1
nmap <leader>2 <Plug>AirlineSelectTab2
nmap <leader>3 <Plug>AirlineSelectTab3
nmap <leader>4 <Plug>AirlineSelectTab4
nmap <leader>5 <Plug>AirlineSelectTab5
nmap <leader>6 <Plug>AirlineSelectTab6
nmap <leader>7 <Plug>AirlineSelectTab7
nmap <leader>8 <Plug>AirlineSelectTab8
nmap <leader>9 <Plug>AirlineSelectTab9

"" vim-airline-themes
""" Solarized dark theme for vim-airline
let g:airline_solarized_bg = 'dark'

