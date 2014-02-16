" Vim global plugin for marking of inactive blocks in a C/C++ file.
" Maintainer:	Sascha <ext.sascha@gmail.com>
" Version:	0.1
" Description:	This plugin parses C/C++ preprocessing directives and marks inactive blocks in the buffer.
" Last Change:	2014-02-16
" License:	Vim License (see :help license)
" Location:	plugin/
" Website:	https://github.com//
"
" See .txt for help.  This can be accessed by doing:
"
" :helptags ~/.vim/doc
" :help 

" Vimscript Setup: {{{1
" Allow use of line continuation.
let s:save_cpo = &cpo
set cpo&vim

" Check for python support
if !has('python')
  echo "Error: CppBlocks plugin requires vim compiled with +python"
  finish
endif

" load guard
" uncomment after plugin development.
"if exists("g:loaded_CppBlocks")
"      \ || &compatible
"  let &cpo = s:save_cpo
"  finish
"endif
"let g:loaded_CppBlocks = 1

" Options: {{{1
if !exists('g:CppBlocks_library_path')
  let g:CppBlocks_library_path = expand('%:h:p') . '/..'
endif

if !exists('g:CppBlocks_python_path')
  let g:CppBlocks_python_path = expand('%:h:p')
endif

if !exists('g:CppBlocks_analyze_headers')
  let g:CppBlocks_analyze_headers = 0
endif

if !exists('g:CppBlocks_include_dirs_angle')
  let g:CppBlocks_include_dirs_angle = []
endif

if !exists('g:CppBlocks_include_dirs_quote')
  let g:CppBlocks_include_dirs_quote = []
endif

if !exists('g:CppBlocks_defines')
  let g:CppBlocks_defines = {}
endif

" Load python side: {{1
python import sys
exe 'python sys.path.append("' . g:CppBlocks_library_path . '")'
exe 'python sys.path.append("' . g:CppBlocks_python_path . '")'
python import cppblocks_plugin

" Private Functions: {{{1
function! s:MarkDisabledCppBlocks()
  python cppblocks_plugin.markDisabledCppBlocks()
endfunction

" Public Interface: {{{1
function! MyPublicFunction()
  echom "change MyPublicFunction"
endfunction

" Maps: {{{1
nnoremap <Plug>1 :call <SID>MyScriptLocalFunction()<CR>
nnoremap <Plug>2 :call MyPublicFunction()<CR>

if !hasmapto('<Plug>1')
  nmap <unique><silent> <Leader>p1 <Plug>1
endif

if !hasmapto('<Plug>2')
  nmap <unique><silent> <Leader>p2 <Plug>2
endif

" Commands: {{{1
command! -nargs=0 -bar CppBlocks call <SID>MarkDisabledCppBlocks()
command! -nargs=0 -bar MyCommand2 call MyPublicFunction()

" Teardown: {{{1
" reset &cpo back to users setting
let &cpo = s:save_cpo

" Template From: https://github.com/dahu/Area-41/
" vim: set sw=2 sts=2 et fdm=marker:
