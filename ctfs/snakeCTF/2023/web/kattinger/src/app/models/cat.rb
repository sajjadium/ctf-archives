class Cat < ApplicationRecord
    has_many :comments
    validates :description, presence: true
    validates :location, presence: true
end
