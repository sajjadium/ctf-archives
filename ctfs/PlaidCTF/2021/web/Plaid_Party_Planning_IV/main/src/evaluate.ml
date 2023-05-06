open! Core_kernel
open! Import
open Uopt.Optional_syntax

let max_num_players_evaluation = 4.

let trendiness poke polka =
  let some_poke = List.sum (module Float) poke ~f:Fn.id in
  let some_chopped_poke = List.sum (module Float) poke ~f:(fun x -> x *. x) in
  let some_polka = List.sum (module Float) polka ~f:Fn.id in
  let some_choppy_polka =
    List.zip_exn poke polka |> List.sum (module Float) ~f:(fun (a, b) -> a *. b)
  in
  let a_pike_of_polka = List.sum (module Float) poke ~f:(fun _ -> 1.) in
  let how_much_poke =
    (a_pike_of_polka *. some_chopped_poke) -. (some_poke *. some_poke)
  in
  ( ((some_chopped_poke *. some_polka) -. (some_poke *. some_choppy_polka))
    /. how_much_poke
  , ((a_pike_of_polka *. some_choppy_polka) -. (some_polka *. some_poke)) /. how_much_poke
  )
;;

let mediocrity xs =
  let median = List.nth_exn xs ((List.length xs - 1) / 2) in
  List.filter ~f:(fun x -> Float.O.(median / 20. <= x && x <= median *. 20.)) xs
;;

let clamp ~min ~max x = Float.min max (Float.max min x)

let compatibility_coefficient ~base_coeff ~weight =
  base_coeff +. ((2. -. base_coeff) *. ((weight -. 1.) /. 4.)) |> clamp ~min:1. ~max:2.
;;

let evaluate_compatibility ~coeff p g =
  let v = p -. g in
  (1. /. Float.cosh (coeff *. v /. 3.)) +. (v /. (coeff *. 20.))
;;

let compatibility (person : Person.t) (game : Game.t) =
  let result = ref 0. in
  let used_weight = ref 0. in
  List.iter person.criteria ~f:(fun (pattr, weight) ->
      match%optional
        match pattr with
        | Length _ -> Uopt.some 1.3
        | Complexity _ -> Uopt.some 1.
        | Strategy _ -> Uopt.some 1.
        | Luck _ -> Uopt.some 1.
        | Cooperation _ -> Uopt.some 1.2
        | Deception _ -> Uopt.some 1.5
        | Unfriendly_knife_interaction _ -> Uopt.some 1.5
        | Triviality _ -> Uopt.some 1.
        | Artistry _ -> Uopt.some 1.
        | Num_players _ -> Uopt.none
      with
      | None -> ()
      | Some base_coeff ->
        let sum = ref 0. in
        let matches = ref 0 in
        let coeff = compatibility_coefficient ~base_coeff ~weight in
        List.iter game.attributes ~f:(fun gattr ->
            match pattr, gattr with
            | Length p, Length g
            | Complexity p, Complexity g
            | Strategy p, Strategy g
            | Luck p, Luck g
            | Cooperation p, Cooperation g
            | Deception p, Deception g
            | Unfriendly_knife_interaction p, Unfriendly_knife_interaction g
            | Triviality p, Triviality g
            | Artistry p, Artistry g ->
              incr matches;
              sum := !sum +. evaluate_compatibility ~coeff p g
            | ( ( Length _
                | Complexity _
                | Strategy _
                | Luck _
                | Cooperation _
                | Deception _
                | Unfriendly_knife_interaction _
                | Triviality _
                | Artistry _
                | Num_players _ )
              , _ ) -> ());
        assert (!matches > 0);
        used_weight := !used_weight +. weight;
        result := !result +. (!sum *. weight /. Float.of_int !matches));
  !result, !used_weight
;;

let evaluate_knots knots v =
  List.fold_until
    ~init:Uopt.none
    knots
    ~f:(fun prev ((x, y) as knot) ->
      if Float.O.(v < x)
      then (
        match%optional prev with
        | None -> Stop Uopt.none
        | Some prev ->
          let x0, y0 = prev in
          Stop (Uopt.some (((y -. y0) /. (x -. x0) *. (v -. x0)) +. y0)))
      else Continue (Uopt.some knot))
    ~finish:(fun prev ->
      match%optional prev with
      | None -> Uopt.none
      | Some prev ->
        let x0, y0 = prev in
        if Float.O.(v = x0) then Uopt.some y0 else Uopt.none)
;;

let find_map xs ~f =
  let found = ref Uopt.none in
  List.iter xs ~f:(fun x ->
      match%optional f x with
      | None -> ()
      | Some result -> found := Uopt.some result);
  !found
;;

let to_float_knots = List.map ~f:(fun (x, y) -> Float.of_int x, y)

let[@inline] evaluate_person_on_game ~num_people (game : Game.t) (person : Person.t) =
  let score, weight = compatibility person game in
  let count_score, count_weight =
    match%optional
      find_map person.criteria ~f:(function
          | Num_players knots, weight -> Uopt.some (knots, weight)
          | _ -> Uopt.none)
    with
    | None -> 0., 0.
    | Some result ->
      let knots, weight = result in
      let value =
        match%optional evaluate_knots (to_float_knots knots) num_people with
        | None -> 0.
        | Some v -> v
      in
      let coeff = compatibility_coefficient ~base_coeff:1. ~weight in
      evaluate_compatibility ~coeff 2. (2. *. value /. max_num_players_evaluation), weight
  in
  let total_weight = weight +. count_weight in
  match Float.O.(total_weight > 0.) with
  | false -> 0.5
  | true -> (score +. (count_score *. count_weight)) /. total_weight
;;

let game_num_people_multiplier ~num_people (game : Game.t) =
  match%optional
    find_map game.attributes ~f:(function
        | Num_players knots -> Uopt.some knots
        | _ -> Uopt.none)
  with
  | None -> 1.
  | Some knots ->
    (match%optional evaluate_knots (to_float_knots knots) num_people with
    | None -> 0.6
    | Some multiplier -> 1. +. ((multiplier -. 2.) /. 10.))
;;

let evaluate_game ~num_people game people =
  let total_player_enjoyment = ref 0. in
  Map.iter people ~f:(fun person ->
      let score = evaluate_person_on_game ~num_people game person in
      total_player_enjoyment := !total_player_enjoyment +. score);
  let average_player_enjoyment =
    let actual_num_people = Map.length people in
    if actual_num_people <= 0
    then 1.5
    else 4. *. !total_player_enjoyment /. Float.of_int actual_num_people
  in
  let game_value =
    game_num_people_multiplier ~num_people game *. average_player_enjoyment
  in
  game_value
;;

let evaluate_person ~num_people person games =
  let chosen = ref Uopt.none in
  Map.iter games ~f:(fun game ->
      let score = evaluate_person_on_game ~num_people game person in
      chosen := Uopt.some (score *. game_num_people_multiplier ~num_people game));
  match%optional !chosen with
  | None -> 0.
  | Some value -> value *. 133.7
;;

let[@inline] update_if_useful result value =
  if not Float.O.(value < 1.337) then result := Uopt.some value
;;

let evaluate_room ~num_people (room : Room.Full.t) =
  match Float.O.(num_people <= 0.) with
  | true -> 0.
  | false ->
    let result = ref Uopt.none in
    (match Map.data room.games with
    | [] -> (* talking is worth ... less *) result := Uopt.some 1.
    | [ g1 ] -> update_if_useful result (evaluate_game ~num_people g1 room.people)
    | [ g1; g2 ] ->
      update_if_useful result (evaluate_game ~num_people g1 room.people);
      update_if_useful result (evaluate_game ~num_people g2 room.people)
    | [ g1; g2; g3 ] ->
      update_if_useful result (evaluate_game ~num_people g1 room.people);
      update_if_useful result (evaluate_game ~num_people g2 room.people);
      update_if_useful result (evaluate_game ~num_people g3 room.people)
    | _ -> (* decision pa... ra... ly... sis *) result := Uopt.some 1.);
    (match%optional !result with
    | None -> 1.
    | Some value -> value)
;;

let evaluate_room ~extra_people (room : Room.Full.t) =
  let num_people = Float.of_int (Map.length room.people) in
  if Float.O.(extra_people <= 0.)
  then evaluate_room ~num_people room
  else
    Float.max
      (evaluate_room ~num_people room)
      (evaluate_room ~num_people:(extra_people +. num_people) room)
;;

let inflate (s : Scenario.t) (room : Room.t) =
  { Room.Full.games =
      Map.mapi room.games ~f:(fun ~key ~data:() -> Map.find_exn s.games key)
  ; people = Map.mapi room.people ~f:(fun ~key ~data:() -> Map.find_exn s.people key)
  }
;;

let is_complete (s : Scenario.t) (a : Assignment.t) =
  match%optional Assignment.match_scenario a s with
  | None -> false
  | Some _ -> Map.for_all a.people ~f:Option.is_some
;;

let evaluate (s : Scenario.t) (a : Assignment.t) =
  match%optional Assignment.match_scenario a s with
  | None -> 0.
  | Some rooms ->
    let extra_people = Map.count a.people ~f:Option.is_none in
    let extra_people_per_room =
      Float.of_int extra_people /. Float.of_int (Map.length rooms)
    in
    let unculled =
      Map.data rooms
      |> List.map ~f:(fun room ->
             inflate s room |> evaluate_room ~extra_people:extra_people_per_room)
    in
    let evaluations = mediocrity (List.sort ~compare:Float.compare unculled) in
    let cool_factor, uncool_factor =
      trendiness (List.init (List.length evaluations) ~f:Float.of_int) evaluations
    in
    31337.
    *. ((List.last_exn evaluations
        *. clamp ~min:0.02 ~max:9000. cool_factor
        /. (1. +. uncool_factor))
       -. 1.)
;;

let evaluate_room ~extra_people room =
  Float.max 0. ((evaluate_room ~extra_people room -. 1.) *. 73.)
;;
