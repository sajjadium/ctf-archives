class User < ApplicationRecord
    has_many :comments
    validates :username, presence: true, length: {maximum: 8}  # We have to save space!!
    validates :password, presence: true, length: {minimum: 16} # but we care about security
end
