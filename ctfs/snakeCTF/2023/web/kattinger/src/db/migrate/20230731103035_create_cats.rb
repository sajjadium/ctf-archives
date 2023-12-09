class CreateCats < ActiveRecord::Migration[7.0]
  def change
    create_table :cats do |t|
      t.string :description
      t.string :location

      t.timestamps
    end
  end
end
