#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sascha <ext.sascha@gmail.com>
#
# Distributed under terms of the MIT license.

"""
This is the Python part of the Vim plugin 'CppBlocks'.

It invokes the CppBlocks Python library on a file and transfers the list of
disabled blocks back to Vim.
"""
import vim
import cppblocks

def markDisabledCppBlocks():
    filepath = vim.current.buffer.name
    analyzeHeaders = bool(vim.vars["CppBlocks_analyze_headers"])
    includeDirsAngle = vim.vars["CppBlocks_include_dirs_angle"]
    includeDirsQuote = vim.vars["CppBlocks_include_dirs_quote"]
    initialDefines = vim.vars["CppBlocks_defines"]

    #vim.vars["disabledBlocks"] = cppblocks.getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)
    disabledBlocks = cppblocks.getDisabledBlocks(filepath, analyzeHeaders, includeDirsAngle, includeDirsQuote, initialDefines)

    highlightAllDisabledCppBlocks(disabledBlocks)

def highlightAllDisabledCppBlocks(disabledBlocks):
    for disabledBlocksInFile in disabledBlocks.itervalues():
        highlightDisabledCppBlocks(disabledBlocksInFile)

def highlightDisabledCppBlocks(disabledBlocks):
    vim.command('syntax clear CppBlocks_DisabledBlocks')
    for block in disabledBlocks:
        vim.command(r'syntax region CppBlocks_DisabledBlocks start=/\%{0}l/ end=/\%{1}l/'.format(block[0], block[0]+block[1]))
