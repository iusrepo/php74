# Makefile for source rpm: php
# $Id$
NAME := php
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
