#!/bin/bash
vagrant box remove babyvm
rm package.box
vagrant destroy
vagrant up
vagrant halt
vagrant package
vagrant box add --name babyvm package.box
