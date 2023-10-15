#!/bin/sh

# remove the session every 5 minutes
while true; do
    rm -r ./writable/session/*
    rm -r ./writable/debugbar/*

    sleep 10;

    php spark migrate

    sleep 5m
done
