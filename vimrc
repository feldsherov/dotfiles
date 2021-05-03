" Turn on syntax highlighting.
syntax on

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

" Disable the default Vim startup message.
set shortmess+=I

" The backspace key has slightly unintuitive behavior by default. For example,
" by default, you can't backspace before the insertion point set with 'i'.
" This configuration makes backspace behave more reasonably, in that you can
" backspace over anything.
set backspace=indent,eol,start

" code specific
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab

" highlight search result
set hlsearch

" Plug related stuff
call plug#begin('~/.vim/plugged')

" vim visual setup
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'ntpeters/vim-better-whitespace'
Plug 'chriskempson/base16-vim'
Plug 'bogado/file-line'

" generic library
Plug 'mattn/webapi-vim'

" git integration
Plug 'airblade/vim-gitgutter'

" navigation between vim aand tmux
Plug 'christoomey/vim-tmux-navigator'

" github gist integration
Plug 'mattn/vim-gist'

" rust tools
Plug 'rust-lang/rust.vim'
Plug 'cespare/vim-toml'


" nginx config files syntax highlite
Plug 'chr4/nginx.vim'

" fast switch between cpp/h files
Plug 'derekwyatt/vim-fswitch'

" laanguage server integration
Plug 'neoclide/coc.nvim', {'branch': 'release'}


" cland-format support, i have no
" good clang format config. so do not use it.
" Plug 'rhysd/vim-clang-format'

" vim flake8 support. I have no
" good python linter configs.
" Plug 'nvie/vim-flake8'

call plug#end()

" airline setup
let g:airline#extensions#tabline#enabled = 1

noremap <Leader>rf :RustFmt<CR>
vnoremap <Leader>rf :RustFmtRange<CR>

noremap <F3> :Autoformat<CR>

noremap <Leader>of :FSHere<CR>

" 81 collumn is read
set colorcolumn=81

" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" chop trailing whitespaces
let g:strip_whitespace_on_save=1
" enable whitespace highlite

highlight ExtraWhitespace ctermbg=gray
let g:better_whitespace_enabled=1
