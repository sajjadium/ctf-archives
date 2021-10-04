#!/bin/sh

cd /tmp/$1
dotnet publish -c Release 
