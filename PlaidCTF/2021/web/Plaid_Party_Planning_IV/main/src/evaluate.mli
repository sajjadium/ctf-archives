open! Core_kernel
open! Import

val evaluate_person_on_game : num_people:float -> Game.t -> Person.t -> float
val evaluate_game : num_people:float -> Game.t -> Person.t Person_id.Map.t -> float
val evaluate_person : num_people:float -> Person.t -> Game.t Game_id.Map.t -> float
val inflate : Scenario.t -> Room.t -> Room.Full.t
val evaluate_room : extra_people:float -> Room.Full.t -> float
val evaluate : Scenario.t -> Assignment.t -> float
val is_complete : Scenario.t -> Assignment.t -> bool
