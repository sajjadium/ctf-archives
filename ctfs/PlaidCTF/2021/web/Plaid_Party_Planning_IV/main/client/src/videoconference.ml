open! Core_kernel
open! Bonsai_web
open! Bonsai.Let_syntax
open! Pppiv_lib

module Draggable = struct
  type t =
    | Game of Game_id.t
    | Person of Person_id.t
  [@@deriving sexp, equal]
end

module Target = struct
  type t = Room_id.t option [@@deriving sexp, equal]
end

module Assignment_update = struct
  type t =
    | Place of Draggable.t * Target.t
    | Randomize
    | Reset
  [@@deriving sexp]
end

let scenario = Scenario.default

let update_assignment
    ~inject:_
    ~schedule_event:_
    (model : Assignment.t)
    (action : Assignment_update.t)
  =
  match action with
  | Place (Game key, data) -> { model with games = Map.set model.games ~key ~data }
  | Place (Person key, data) -> { model with people = Map.set model.people ~key ~data }
  | Randomize -> Assignment.randomize model scenario
  | Reset -> Assignment.of_scenario scenario
;;

module Random_comp (M : sig
  type t [@@deriving sexp, hash, compare]

  val to_string : t -> string
end)
() =
struct
  type t = M.t [@@deriving sexp]

  let compare =
    Comparable.lexicographic
      [ Comparable.lift Bool.compare ~f:(fun x ->
            not (String.equal (M.to_string x) "strikeskids"))
      ; Comparable.lift Int.compare ~f:M.hash
      ; M.compare
      ]
  ;;

  include (val Comparator.make ~sexp_of_t ~compare)
end

module Game_id_random_comp = Random_comp (Game_id) ()
module Person_id_random_comp = Random_comp (Person_id) ()

let unplaced_games model =
  let%sub { Assignment.games; _ } = Bonsai.read model in
  return
  @@ let%map games = games in
     Map.to_alist games
     |> List.filter_map ~f:(fun (k, v) -> if Option.is_none v then Some (k, ()) else None)
     |> Map.of_alist_exn (module Game_id_random_comp)
;;

let unplaced_people model =
  let%sub { Assignment.people; _ } = Bonsai.read model in
  return
  @@ let%map people = people in
     Map.to_alist people
     |> List.filter_map ~f:(fun (k, v) -> if Option.is_none v then Some (k, ()) else None)
     |> Map.of_alist_exn (module Person_id_random_comp)
;;

let rooms (model : Assignment.t Bonsai.Value.t) =
  return
  @@ let%map model = model in
     Assignment.rooms ~all_rooms:scenario.rooms model
;;

let dragging_to_attr (d : Drag_and_drop.state) =
  match d with
  | Dragging -> Vdom.Attr.class_ "dragging"
  | Not_dragging -> Vdom.Attr.empty
;;

let game_icon game =
  Vdom.Node.create
    "img"
    Vdom.Attr.[ class_ "game-icon"; src (Game.icon_path game); title (Game.name game) ]
    []
;;

let unplaced_game dnd id =
  let%sub dnd = Drag_and_drop.item (module Game_id) dnd id in
  return
  @@ let%map id = id
     and dnd_attr, dragging = dnd in
     let game = Map.find_exn scenario.games id in
     Vdom.Node.div
       Vdom.Attr.[ dnd_attr @ dragging_to_attr dragging @ class_ "unplaced-game" ]
       [ game_icon game
       ; Vdom.Node.div
           Vdom.Attr.[ class_ "game-name" ]
           [ Vdom.Node.text (Game.name game) ]
       ]
;;

let room_game dnd id game =
  let%sub dnd = Drag_and_drop.item (module Game_id) dnd id in
  return
  @@ let%map dnd_attr, dragging = dnd
     and game = game in
     Vdom.Node.div
       Vdom.Attr.[ dnd_attr @ dragging_to_attr dragging @ class_ "room-game" ]
       [ game_icon game ]
;;

let avatar (person : Person.t) =
  let { Person.src = source; content_type = _ } = List.hd_exn person.avatar in
  Vdom.Node.div
    Vdom.Attr.[ class_ "avatar" ]
    [ Vdom.Node.create
        "video"
        Vdom.Attr.
          [ create "playsinline" ""
          ; create "autoplay" ""
          ; create "loop" ""
          ; string_property "muted" "muted"
          ; src source
          ]
        []
    ]
;;

let unplaced_person dnd id =
  let%sub dnd = Drag_and_drop.item (module Person_id) dnd id in
  return
  @@ let%map id = id
     and dnd_attr, dragging = dnd in
     let person = Map.find_exn scenario.people id in
     Vdom.Node.div
       Vdom.Attr.[ dnd_attr @ dragging_to_attr dragging @ class_ "unplaced-person" ]
       [ avatar person
       ; Vdom.Node.div
           Vdom.Attr.[ class_ "person-name" ]
           [ Vdom.Node.text (Person.name person) ]
       ]
;;

let room_person ~(room : Room.Full.t Bonsai.Value.t) ~extra_people dnd id person =
  let%sub dnd = Drag_and_drop.item (module Person_id) dnd id in
  let score =
    let%map person = person
    and room = room
    and extra_people = extra_people in
    let num_people = Float.of_int (Map.length room.people) in
    Float.max
      (Evaluate.evaluate_person ~num_people person room.games)
      (Evaluate.evaluate_person
         ~num_people:(num_people +. extra_people)
         person
         room.games)
  in
  return
  @@ let%map dnd_attr, dragging = dnd
     and score = score
     and person = person in
     Vdom.Node.div
       Vdom.Attr.[ dnd_attr @ dragging_to_attr dragging @ class_ "room-person" ]
       [ avatar person
       ; Vdom.Node.div
           Vdom.Attr.[ class_ "person-name" ]
           [ Vdom.Node.textf !"%s: %.0f" (Person.name person) score ]
       ]
;;

let room_people people =
  let grid_size =
    List.find [ 1; 2; 3 ] ~f:(fun x -> x * x >= Map.length people)
    |> Option.value ~default:4
  in
  let grid_template = sprintf "repeat(%d, 1fr)" grid_size in
  Vdom.Node.div
    Vdom.Attr.[ class_ "room-people-container" ]
    [ Vdom.Node.div Vdom.Attr.[ class_ "room-people-sizing" ] []
    ; Vdom.Node.div
        Vdom.Attr.
          [ class_ "room-people"
          ; style
              Css_gen.(
                create ~field:"grid-template-rows" ~value:grid_template
                @> create ~field:"grid-template-columns" ~value:grid_template)
          ]
        (Map.data people)
    ]
;;

let room_view ~extra_people ~dnd_games ~dnd_people id room =
  let target =
    let%map id = id in
    Some id
  in
  let%sub ({ Room.Full.people; games } as room) =
    let%sub room = Bonsai.Incr.value_cutoff ~equal:phys_equal room in
    return
    @@ let%map room = room in
       Evaluate.inflate scenario room
  in
  let%sub games =
    Bonsai.assoc
      (module Game_id)
      games
      ~f:(fun id (game : Game.t Bonsai.Value.t) -> room_game dnd_games id game)
  in
  let%sub people =
    Bonsai.assoc
      (module Person_id)
      people
      ~f:(fun id (person : Person.t Bonsai.Value.t) ->
        room_person ~room ~extra_people dnd_people id person)
  in
  let score =
    let%map extra_people = extra_people
    and room = room in
    Float.max
      (Evaluate.evaluate_room ~extra_people room)
      (Evaluate.evaluate_room ~extra_people:0. room)
  in
  let%sub dnd_games = Drag_and_drop.target (module Target) dnd_games target in
  let%sub dnd_people = Drag_and_drop.target (module Target) dnd_people target in
  return
  @@ let%map games = games
     and people = people
     and attr1, item1 = dnd_games
     and attr2, item2 = dnd_people
     and score = score in
     let dnd_attrs =
       Vdom.Attr.(
         attr1
         @ attr2
         @
         if Option.is_some item1 || Option.is_some item2
         then class_ "drop-target"
         else empty)
     in
     Vdom.Node.div
       Vdom.Attr.[ dnd_attrs @ class_ "room" ]
       [ Vdom.Node.div Vdom.Attr.[ class_ "room-games" ] (Map.data games)
       ; room_people people
       ; Vdom.Node.div Vdom.Attr.[ class_ "room-score" ] [ Vdom.Node.textf "%.0f" score ]
       ]
;;

let unplaced_view cmp dnd attr data ~f =
  let%sub subviews =
    Bonsai.assoc cmp data ~f:(fun el (_ : unit Bonsai.Value.t) -> f dnd el)
  in
  let%sub dnd = Drag_and_drop.target (module Target) dnd (Bonsai.Value.return None) in
  return
  @@ let%map subviews = subviews
     and dnd_attr, item = dnd in
     Map.data subviews
     |> Vdom.Node.div
          Vdom.Attr.
            [ (dnd_attr
              @ attr
              @
              match item with
              | None -> empty
              | Some _ -> class_ "drop-target")
            ]
;;

let score_view score =
  return
  @@ let%map score = score in
     Vdom.Node.div
       Vdom.Attr.[ class_ "score" ]
       [ Vdom.Node.textf "%08d" (Int.of_float score) ]
;;

let handle_submission ~messages =
  let%sub pending, set_pending =
    Bonsai.state [%here] ~default_model:false (module Bool)
  in
  let submit =
    let%map messages = messages
    and set_pending = set_pending in
    let on_response result =
      let message =
        match (result : Protocol.Submit_assignment.Response.t Or_error.t) with
        | Error e -> sprintf !"%{Error#hum}" e
        | Ok (Invalid e) -> sprintf !"Invalid: %{Error#hum}" e
        | Ok (Valid { flag = None }) -> sprintf "Submitted!"
        | Ok (Valid { flag = Some flag }) -> sprintf "Flag: %s" flag
      in
      Ui_event.Many
        [ set_pending false
        ; Effect.inject
            ~on_response:(fun _ -> Ui_event.Ignore)
            (Info_popup.show messages message)
        ]
    in
    fun effect -> Ui_event.Many [ Effect.inject effect ~on_response; set_pending true ]
  in
  return
  @@ let%map submit = submit
     and pending = pending in
     not pending, submit
;;

let actions ~submit_assignment ~can_submit ~update_assignment ~score ~assignment:assn =
  let%sub submit =
    Header.button
      ~on_click:
        (let%map submit_assignment = submit_assignment in
         fun _ -> submit_assignment)
      ~enabled:
        (let%map assn = assn
         and score = score
         and can_submit = can_submit in
         Evaluate.is_complete scenario assn && Float.O.(score > 0.) && can_submit)
      (Bonsai.Value.return "Submit")
  in
  let%sub reset =
    Header.button
      ~on_click:
        (let%map f = update_assignment in
         fun _ -> f Assignment_update.Reset)
      (Bonsai.Value.return "Reset")
  in
  let%sub randomize =
    Header.button
      ~on_click:
        (let%map f = update_assignment in
         fun _ -> f Assignment_update.Randomize)
      (Bonsai.Value.return "Randomize")
  in
  return
  @@ let%map reset = reset
     and randomize = randomize
     and submit = submit in
     [ reset; randomize; submit ]
;;

let view ~submit_assignment ~messages =
  let%sub assignment, inject =
    Bonsai.state_machine0
      [%here]
      (module Assignment)
      (module Assignment_update)
      ~apply_action:update_assignment
      ~default_model:(Assignment.of_scenario scenario)
  in
  let%sub can_submit, run_submit = handle_submission ~messages in
  let submit_assignment =
    let%map assignment = assignment
    and run_submit = run_submit
    and submit_assignment = submit_assignment in
    run_submit (submit_assignment assignment)
  in
  let%sub dnd_games =
    Drag_and_drop.create
      (module Game_id)
      (module Target)
      ~on_drop:
        (let%map inject = inject in
         fun g room -> inject (Place (Game g, room)))
  in
  let%sub dnd_people =
    Drag_and_drop.create
      (module Person_id)
      (module Target)
      ~on_drop:
        (let%map inject = inject in
         fun p room -> inject (Place (Person p, room)))
  in
  let%sub unplaced_games = unplaced_games assignment in
  let%sub unplaced_people = unplaced_people assignment in
  let%sub rooms = rooms assignment in
  let%sub game_view =
    unplaced_view
      (module Game_id_random_comp)
      dnd_games
      (Vdom.Attr.class_ "unplaced-games")
      unplaced_games
      ~f:unplaced_game
  in
  let%sub people_view =
    unplaced_view
      (module Person_id_random_comp)
      dnd_people
      (Vdom.Attr.class_ "unplaced-people")
      unplaced_people
      ~f:unplaced_person
  in
  let extra_people =
    let%map unplaced_people = unplaced_people in
    Float.of_int (Map.length unplaced_people) /. Float.of_int (Set.length scenario.rooms)
  in
  let%sub room_views =
    Bonsai.assoc
      (module Room_id)
      rooms
      ~f:(room_view ~extra_people ~dnd_games ~dnd_people)
  in
  let score =
    let%map assn = assignment in
    Evaluate.evaluate scenario assn
  in
  let%sub score_change = Score_changes.view score in
  let%sub score_view = score_view score in
  let%sub actions =
    actions ~submit_assignment ~can_submit ~update_assignment:inject ~assignment ~score
  in
  return
  @@ let%map game_view = game_view
     and people_view = people_view
     and room_views = room_views
     and score_change = score_change
     and score_view = score_view
     and actions = actions in
     ( Vdom.Node.div
         Vdom.Attr.[ class_ "videoconference" ]
         ([ game_view ] @ Map.data room_views @ [ people_view ])
     , [ score_view; score_change ]
     , actions )
;;
