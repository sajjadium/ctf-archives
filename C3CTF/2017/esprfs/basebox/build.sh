#!/bin/bash
rm -f package.box
vagrant box remove esprfsvm
vagrant destroy
vagrant up
vagrant halt
vagrant package 
vagrant box add --name esprfsvm package.box
