#include <iostream>
#include <map>
#include <string>
#include <fstream>
#include <streambuf>

#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

// Amount of money the player has
unsigned long long player_funds = 150;

// Time for one tick of mining. Ten per operation
unsigned int tool_time = 500000;

// Mining profit per operation
unsigned int mining_profit = 10;

// The number of replacements the player has
unsigned int tools_left = 0;

// Mining operations before player is no longer encouraged
unsigned int encouragement = 0;

std::string name;

void place_bet(){
	if(player_funds == 0){
		std::cout << "You don't have enough money for this!" << std::endl;
		return;
	}
	std::cout << "A coin will be flipped. Before the coin is flipped, you may pick heads or tails. "
		<< "If you guess correctly, any money you bet will be doubled. Otherwise, the money will"
		<< " be forfeit. Enter heads, tails, or cancel" << std::endl;
	std::string input;
	std::cin >> input;
	if(input == "heads" || input == "tails"){
		unsigned long long bet{ 0 };
		
		do {
			std::cout << "How much would you like to bet that the coin will come up " << input << "?"
				<< " Enter a number between 1 and " << player_funds << "." << std::endl;
			std::cin >> bet;
		} while(!std::cin.good() || bet > player_funds);

		player_funds -= bet;

		srand(time(nullptr));
		auto val{ rand() % 2 };
		if(val){
			std::cout << "... and the coin came up " << input << "!! You just got $" << bet
			       <<"! Congratulations! Your balance is $" << (player_funds += bet * 2) << std::endl;
		} else {
			std::cout << "... and the coin came up " << (input == "heads" ? "tails" : "heads") 
				<< ". You lost $" << bet << ". Your balance is $" << player_funds << std::endl;
		}
	} else {
		std::cout << "Cancelling bet" << std::endl;
	}
}

void tool_break(){
	std::cout << "Oh no! Your tool broke!";
	if(tools_left == 0){
		std::cout << " You don't have any replacements available. It's back to mining with your hands" << std::endl;
		mining_profit = 10;
	} else {
		std::cout << " You used a replacement. You now have " << --tools_left << " replacements available " << std::endl;
	}
}

void work(){
	std::cout << "You go to work in the mines" << std::endl;
	std::cout << "[..........]" << std::endl;
	for(unsigned int i = 0; i < 10; i++){
		usleep(tool_time);
		std::cout << "[";
		for(unsigned int j = 0; j <= i; j++){
			std::cout << "=";
		}
		for(unsigned int j = i + 1; j < 10; j++){
			std::cout << ".";
		}
		std::cout << "]" << std::endl;
	}

	srand(time(NULL));
	
	if(rand() % 100 == 0){
		auto profit{ mining_profit * 9 + rand() % (2 * mining_profit) };
		std::cout << "You struck gold! You earned $" << profit << ". Your balance is now $"
		       << (player_funds += profit) << ". " << std::endl;
	} else {
		auto profit{ 1 + rand() % (2 * mining_profit) };
		std::cout << "It was a normal days work. You earned $" << profit << ". Your balance is now $"
			<< (player_funds += profit) << ". " << std::endl;
	}

	if(rand() % 3 == 0 && mining_profit != 10){
		tool_break();
	}

	if(encouragement){
		encouragement--;
		if(encouragement == 0){
			std::cout << "You aren't encouraged to mine faster anymore" << std::endl;
			tool_time = 500000;
		}
	}
}

void purchase(){
	std::map<std::string, unsigned long long> prices{
		{ "tool", 100 },
		{ "encouragement", 20 },
		{ "shout-out-from-literally-god", 1000000000000000ULL }
	};

	std::string option{};
	do {
		std::cout << "What would you like to buy? Options are ";
		for(auto& entry : prices){
			std::cout << entry.first << " (cost: " << entry.second << "), ";
		}
		std::cout << "or cancel" << std::endl;
		std::cin >> option;
		if(option == "cancel"){
			return;
		}
	} while(prices.find(option) == prices.end());

	unsigned long long count{ 0 };
	do {
		std::cout << "How many would you like to buy? Must be greater than 0" << std::endl;
		std::cin >> count;
	} while(!std::cin.good() || !count);

	auto item_cost{ prices.at(option) };
	auto total{ item_cost * count };
	if(total > player_funds) {
		std::cout << "You don't have the money for that!" << std::endl;
		return;
	}

	player_funds -= total;
	if(option == "tool"){
		std::cout << "You bought " << count << " tool" << ((count - 1) ? "s" : "") << ". You " 
			<< "now have " << (tools_left += count - 1) << " spare tool" 
			<< (tools_left - 1 ? "s" : "") << std::endl;
		mining_profit = 50;
	} else if(option == "encouragement"){
		for(unsigned long long i = 0; i < count; i++){
			std::cout << "You can do it! Go you!" << std::endl;
			encouragement++;
		}
		std::cout << "You are now very encouraged! Your mining speed has increased." << std::endl;
		tool_time = 50000;
	} else if(option == "shout-out-from-literally-god"){
		bool god_is_happy = rand() & 0xFFFFFF == 0;
		bool* god_is_really_happy = &god_is_happy;
		printf("Hmmmm\n");
		printf(name.c_str());
		printf("\nYou have done well!\n");
		printf("Good job!\n");
		
		if(*god_is_really_happy){
			printf("I'm feeling generous right now!\nHave a flag!\n");
			std::ifstream t("flag.txt");
			std::string str((std::istreambuf_iterator<char>(t)),
				                 std::istreambuf_iterator<char>());
			std::cout << str << std::endl;
		}

		printf("Sincerely,\n");
		printf("\t~God\n");
	}
}

int main(int argc, char** argv){
	std::cout << "Welcome to this very in-depth game. The goal is to amass wealth and earn the god's favor." << std::endl;
	std::cout << "Before we continue, what is your name?" << std::endl;
	std::cin >> name;

	do {
		std::cout << "Current funds: $" << player_funds << std::endl;
		std::cout << "Your options are: " << std::endl;
		std::cout << "1: Place a bet on a coin flip for a chance to double your money" << std::endl;
		std::cout << "2: Go mining to earn some money" << std::endl;
		std::cout << "3: Buy things" << std::endl;
		std::cout << "4: Quit (Your money will not be saved)" << std::endl;
		std::cout << "Please enter a number 1-4 to continue..." << std::endl;
		std::string input{};
		std::cin >> input;
		if(input == "1"){
			place_bet();
		} else if(input == "2"){
			work();
		} else if(input == "3"){
			purchase();
		} else if(input == "4"){
			return 0;
		} else {
			std::cout << "Invalid input" << std::endl;
		}
	} while(true);
}
