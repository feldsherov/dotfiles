" Turn off arrows
noremap <Up> <NOP>
noremap <Down> <NOP>
noremap <Left> <NOP>
noremap <Right> <NOP>

" Line numbers
set number

" Fix backspace on Mac OS
set backspace=2

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
