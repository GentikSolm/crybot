default:
    @just --list

GREEN  := "\\u001b[32m"
RESET  := "\\u001b[0m"
CHECK  := `/usr/bin/printf "\xE2\x9C\x94"`

build:
    @docker compose build

up: build
    @docker compose up -d

test: build
    @echo -e " {{GREEN}}{{CHECK}} All tests passed! {{CHECK}} {{RESET}}"
