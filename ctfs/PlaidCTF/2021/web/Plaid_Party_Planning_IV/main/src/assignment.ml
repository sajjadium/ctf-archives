open! Core_kernel
open! Import

type t =
  { games : Room_id.t option Game_id.Map.t
  ; people : Room_id.t option Person_id.Map.t
  }
[@@deriving bin_io, sexp, equal, fields]

let of_scenario (scenario : Scenario.t) =
  { games = Map.map scenario.games ~f:(fun _ -> None)
  ; people = Map.map scenario.people ~f:(fun _ -> None)
  }
;;

let rooms ~all_rooms t =
  let rooms =
    Map.fold t.games ~init:Room_id.Map.empty ~f:(fun ~key:game ~data:room_id acc ->
        match room_id with
        | None -> acc
        | Some room_id ->
          Map.update acc room_id ~f:(fun room ->
              Option.value room ~default:Room.empty |> Fn.flip Room.add_game game))
  in
  let rooms =
    Map.fold t.people ~init:rooms ~f:(fun ~key:person ~data:room_id acc ->
        match room_id with
        | None -> acc
        | Some room_id ->
          Map.update acc room_id ~f:(fun room ->
              Option.value room ~default:Room.empty |> Fn.flip Room.add_person person))
  in
  let rooms =
    Set.fold ~init:rooms all_rooms ~f:(fun acc room_id ->
        Map.update acc room_id ~f:(Option.value ~default:Room.empty))
  in
  rooms
;;

let match_scenario (a : t) (s : Scenario.t) =
  let people_equal = Person_id.Set.equal (Map.key_set s.people) (Map.key_set a.people) in
  let games_equal = Game_id.Set.equal (Map.key_set s.games) (Map.key_set a.games) in
  let rooms = rooms ~all_rooms:s.rooms a in
  let rooms_equal = Room_id.Set.equal (Map.key_set rooms) s.rooms in
  if people_equal && rooms_equal && games_equal then Uopt.some rooms else Uopt.none
;;

let randomize (a : t) (s : Scenario.t) =
  let games_for_rooms = Map.of_key_set s.rooms ~f:(fun _ -> Random.int_incl 1 3) in
  let to_choose = Map.keys a.games |> Array.of_list in
  let games =
    List.fold
      (List.rev (List.range 0 3))
      ~init:(Map.map ~f:(fun _ -> None) a.games)
      ~f:(fun games minv ->
        Map.fold games_for_rooms ~init:games ~f:(fun ~key:room ~data:allowedv games ->
            if allowedv > minv
            then
              Map.set
                games
                ~key:to_choose.(Random.int (Array.length to_choose))
                ~data:(Some room)
            else games))
  in
  let rooms = Set.to_array s.rooms in
  { games
  ; people = Map.map a.people ~f:(fun _ -> Some rooms.(Random.int (Array.length rooms)))
  }
;;
