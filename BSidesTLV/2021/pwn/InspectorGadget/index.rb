#!/usr/bin/env ruby
# frozen_string_literal: true

require 'csv'
require 'json'
require 'base64'

class DynamicLog
  def initialize(level, message, type)
    @level = level
    @message = message
    @type = type
  end

  def log
    obj = { :level => @level, :message => @message }
    message =
      case @type
      when 'json'
        JSON.dump obj
      when 'csv'
        CSV.generate do |csv|
          csv << obj.keys
          csv << obj.values
        end
      else
        "[#{@level}] #{@message}"
      end
    puts message
  end
end

class Gem::Requirement
  def marshal_load(array) end
end

def firewall(input)
  %w[DynamicLog @type @level @message].each do |word|
    return true unless input.include? word
  end

  %w[
    Gem::Requirement Gem::DependencyList Gem::Requirement
    Gem::StubSpecification Gem::Source::SpecificFile
    ActiveModel::AttributeMethods::ClassMethods::CodeGenerator
    ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy
  ].each do |word|
    return true if input.include? word
  end
  false
end

def main
  puts %(
      ###                                                            #####
       #  #    #  ####  #####  ######  ####  #####  ####  #####     #     #   ##   #####   ####  ###### #####
       #  ##   # #      #    # #      #    #   #   #    # #    #    #        #  #  #    # #    # #        #
       #  # #  #  ####  #    # #####  #        #   #    # #    #    #  #### #    # #    # #      #####    #
       #  #  # #      # #####  #      #        #   #    # #####     #     # ###### #    # #  ### #        #
       #  #   ## #    # #      #      #    #   #   #    # #   #     #     # #    # #    # #    # #        #
      ### #    #  ####  #      ######  ####    #    ####  #    #     #####  #    # #####   ####  ######   #
   )
  log = 'BAhvOg9EeW5hbWljTG9nCDoLQGxldmVsSSIJSU5GTwY6BkVUOg1AbWVzc2FnZUkiDE1lc3NhZ2UGOwdUOgpAdHlwZUkiCGNzdgY7B1Q='
  puts "Please insert log object in base64 format (for example '#{log}'):"
  serialized_object = Base64.decode64 gets
  is_blocked = firewall serialized_object
  puts
  return puts 'Blocked By The Application Firewall' if is_blocked

  Marshal.load(serialized_object).log rescue nil
end

main
