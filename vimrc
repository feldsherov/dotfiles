" Turn off arrows
nnoremap <Left>  :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up>    :echoe "Use k"<CR>
nnoremap <Down>  :echoe "Use j"<CR>
" ...and in insert mode
inoremap <Left>  <ESC>:echoe "Use h"<CR>
inoremap <Right> <ESC>:echoe "Use l"<CR>
inoremap <Up>    <ESC>:echoe "Use k"<CR>
inoremap <Down>  <ESC>:echoe "Use j"<CR>

" This setting makes search case-insensitive when all characters in the string
" being searched are lowercase. However, the search becomes case-sensitive if
" it contains any capital letters. This makes searching more convenient.
set ignorecase
set smartcase

" Enable searching as you type, rather than waiting till you press enter.
set incsearch

" Unbind some useless/annoying default key bindings.
nmap Q <Nop> " 'Q' in normal mode enters Ex mode. You almost never want this.

" Disable audible bell because it's annoying.
set noerrorbells visualbell t_vb=

" Line numbers
set number

" The backspace key has slightly unintuitive behavior by default. For example,
" by default, you can't backspace before the insertion point set with 'i'.
" This configuration makes backspace behave more reasonably, in that you can
" backspace over anything.
set backspace=indent,eol,start

" code specific
set tabstop=2
set shiftwidth=2
set expandtab
set smarttab

" highlighte search result
set hlsearch

" Plug related stuff
call plug#begin('~/.vim/plugged')

Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'ntpeters/vim-better-whitespace'
Plug 'chriskempson/base16-vim'
Plug 'airblade/vim-gitgutter'
Plug 'rhysd/vim-clang-format'
Plug 'PegasusWang/vim-ubuntu-pastebin'
Plug 'nvie/vim-flake8'
Plug 'christoomey/vim-tmux-navigator'
Plug 'cespare/vim-toml'
Plug 'rust-lang/rust.vim'
Plug 'bogado/file-line'
Plug 'derekwyatt/vim-fswitch'
Plug 'mattn/webapi-vim'
Plug 'mattn/vim-gist'
Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install() } }

call plug#end()

" airline setup
let g:airline#extensions#tabline#enabled = 1

" code style
let g:clang_format#code_style='google'
noremap <Leader>cf :ClangFormat<CR>
vnoremap <Leader>cf :ClangFormat<CR>

noremap <Leader>of :FSHere<CR>

" 81 collumn is read
set colorcolumn=81
