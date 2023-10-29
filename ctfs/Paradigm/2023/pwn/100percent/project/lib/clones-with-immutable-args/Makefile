# include .env file and export its env vars
# (-include to ignore error if it does not exist)
-include .env

# deps
update:; forge update

# Build & test
build  :; forge clean && forge build --optimize --optimize-runs 1000000
test   :; forge clean && forge test --optimize --optimize-runs 1000000 -v # --ffi # enable if you need the `ffi` cheat code on HEVM
trace  :; forge clean && forge test --optimize --optimize-runs 1000000 -vvv # --ffi # enable if you need the `ffi` cheat code on HEVM
clean  :; forge clean
snapshot :; forge clean && forge snapshot --optimize --optimize-runs 1000000
lint   :; yarn lint