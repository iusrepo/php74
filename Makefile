# Makefile for source rpm: php
# $Id$
NAME := php
SPECFILE = $(firstword $(wildcard *.spec))
UPSTREAM_CHECKS := 

include ../common/Makefile.common
