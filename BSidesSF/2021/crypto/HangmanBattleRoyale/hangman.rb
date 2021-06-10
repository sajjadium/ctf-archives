#!/usr/bin/env ruby

require_relative './flag'
require 'timeout'
require 'colorize'

$stdout.sync = true

FIRST_NAMES = File.read(File.join(__dir__, 'first-names.txt')).split(/\n/)
LAST_NAMES  = File.read(File.join(__dir__, 'last-names.txt')).split(/\n/)
WORDS       = File.read(File.join(__dir__, 'words.txt')).split(/\n/)

# % chance of outright guessing - this should be low-medium for challenge
CPU_GOOD_GUESS = 30

# % chance of guessing from matching words - this should be fairly high
CPU_BAD_GUESS = 90

# % chance of guessing a good character instead of bad
CPU_INTELLIGENCE = 80

def get_number(prompt = "> ", error = "Invalid number!".red)
  print "> "

  result = gets().to_i

  if !result || result == 0
    puts error
    exit 1
  end

  return result
end

def get_opponents(count)
  return 0.upto(count-1).map do ||
    i = rand(0xFFFFFFFF)
    "#{ FIRST_NAMES[i & 0xFFFF] } #{ LAST_NAMES[i >> 16] }"
  end
end

def player_turn(revealed, word)
  puts
  puts "================================".blue
  puts "          PLAYER TURN".blue
  puts "================================".blue
  puts

  puts
  puts "Enter a letter to guess a letter, or a word to guess the whole thing:"
  puts
  puts "    #{ revealed.chars().map { |c| c.underline() }.join(' ') }"
  puts
  print("Your guess --> ")

  # Get a valid guess
  guess = ''
  loop do
    guess = gets().strip().downcase()
    if guess.length() == 0
      puts "Invalid guess!".red
    else
      break
    end
  end

  # If it's a single letter, reveal it
  if(guess.length() == 1)
    word.chars.each_with_index do |c, i|
      if c == guess
        revealed[i] = word[i]
      end
    end
  else
    if(guess == word)
      revealed = word
    else
      puts "Sorry, that's not correct!".red
    end
  end

  return revealed
end

def computer_turn(revealed, word)
  puts
  puts "================================".blue
  puts "         COMPUTER TURN".blue
  puts "================================".blue
  puts

  puts "    #{ revealed.chars().map { |c| c.underline() }.join(' ') }"
  puts

  known_chars = revealed.chars.select { |c| c != '_' }.sort.uniq
  available_chars = ('a'..'z').to_a - known_chars
  good_chars = word.chars.sort.uniq - known_chars

  # Does the computer "just know"?
  if revealed.index('_').nil? || rand() < (CPU_GOOD_GUESS / 100.0)
    puts "Computer guess --> #{ word }".green
    puts
    puts "It's correct!!".green
    return word
  end

  # Does the computer guess something else?
  if rand() < (CPU_BAD_GUESS / 100.0)
    w = WORDS.select do |w|
      w.match(/^#{ revealed.gsub('_', '.') }$/)
    end

    if w.length() > 0
      guess = w.sample()
      puts "Computer guess --> #{ guess }".green

      if guess == word
        return word
      else
        return revealed
      end
    end
  end

  # Does the computer guess well?
  guess = ''
  if rand() < (CPU_INTELLIGENCE / 100.0)
    guess = good_chars.sample
  else
    guess = available_chars.sample
  end

  puts
  puts "Computer guess --> #{ guess }"
  word.chars.each_with_index do |c, i|
    if c == guess
      revealed[i] = word[i]
    end
  end

  return revealed
end

def play_round(opponents, round)
  # Pick a word
  word = WORDS.sample()

  # Make sure there are an odd number of opponents
  if (opponents.length % 2) == 0
    puts "Somehow, we ended up with an invalid number of opponents!".red
    exit(1)
  end

  puts
  puts "================================".blue
  puts "         ROUND #{round}!".blue
  puts "================================".blue
  puts

  puts "This game's match-ups are:"
  puts
  opponents.each_slice(2) do |s|
    if s.length == 2
      puts "#{ s[0].ljust(20) }  -vs-  #{ s[1] }"
    else
      puts
      puts "And finally..."
      puts
      puts "#{ "YOU".ljust(20) } -vs-  #{ s[0] }!"
    end
  end

  puts
  puts "GOOD LUCK!!"
  puts
  #puts "HINT: #{word}-------------------------------------------------------"


  revealed = '_' * word.length()
  loop do
    revealed = player_turn(revealed, word)
    if revealed.index('_').nil?
      break
    end

    revealed = computer_turn(revealed, word)
    if revealed.index('_').nil?
      puts "Sorry, you lost! Please try again later".red
      exit(0)
    end
  end

  puts
  puts "    #{ revealed.chars().map { |c| c.underline() }.join(' ') }"
  puts

  puts "Congratulations, you beat #{ opponents.pop } and won this round! Let's see how the others did!".green
  puts
  puts "Press enter to continue"
  gets

  # Remove your opponent
  opponents = opponents.each_slice(2).map do |s|
    if rand() < 0.5
      puts "#{ s[0].green } beat #{ s[1].red } and moves on to the next round!"
      s[0]
    else
      puts "#{ s[1].green } beat #{ s[0].red } and moves on to the next round!"
      s[1]
    end
  end

  puts "Press enter to continue"
  gets

  return opponents
end

def start_game()
  puts "Welcome to Hangman Battle Royale!"
  puts
  puts "================================"
  puts "           MAIN MENU"
  puts "================================"
  puts

  puts "How many rounds do you want to play? (2 - 16)"
  puts
  puts "If you play at least 8 rounds, you win the special prize!"
  puts
  rounds = get_number()

  # Opponents are two to the number of rounds
  opponent_count = (2**rounds) - 1
  if opponent_count > 65536
    puts "That's too many rounds!".red
    return
  end

  opponents = get_opponents(opponent_count)
  round = 1
  loop do
    opponents = play_round(opponents, round)

    # If the player losers, play_round returns null
    if !opponents
      puts "Sorry, you lose! :(".red
      return
    end

    if opponents.length() == 0
      puts "You win this round!".green.bold

      if rounds >= 8
        puts "Wow, that was a MEGA victory!".green
        puts "Flag: #{ FLAG }".green
        exit
      end

      return
    end

    round += 1
  end
end

start_game()
