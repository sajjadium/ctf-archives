open! Core_kernel
open! Import

type t =
  { games : Game.t Game_id.Map.t
  ; people : Person.t Person_id.Map.t
  ; rooms : Room_id.Set.t
  }

let slugify name =
  String.lowercase name
  |> String.map ~f:(fun c -> if Char.is_alphanum c then c else '_')
  |> String.split ~on:'_'
  |> List.filter ~f:(fun s -> not (String.is_empty s))
  |> String.concat ~sep:"_"
;;

let nonempty_line s =
  match String.strip s with
  | "" -> None
  | s -> Some s
;;

let mkgames s =
  let get_players s =
    let parts =
      String.split ~on:' ' s |> List.filter ~f:(fun x -> not (String.is_empty x))
    in
    let rec get acc rest =
      match rest with
      | [] -> List.rev acc
      | a :: b :: rest -> get ((Int.of_string a, Float.of_string b) :: acc) rest
      | _ -> failwith "Bad players"
    in
    get [] parts
  in
  let game_of_line line =
    match String.split ~on:'|' line with
    | [ params; name; icon; players ] ->
      let params =
        String.split ~on:' ' params
        |> List.filter ~f:(fun x -> not (String.is_empty x))
        |> List.map ~f:Float.of_string
      in
      let name = String.strip name in
      let id = Game_id.of_string (slugify name) in
      (match params with
      | [ length; complexity; strategy; luck; coop; deception; unf; triviality; artistry ]
        ->
        { Game.id
        ; icon_path = sprintf "games/%s" (String.strip icon)
        ; name
        ; attributes =
            [ Length length
            ; Complexity complexity
            ; Strategy strategy
            ; Luck luck
            ; Cooperation coop
            ; Deception deception
            ; Unfriendly_knife_interaction unf
            ; Triviality triviality
            ; Artistry artistry
            ; Num_players (get_players players)
            ]
        }
      | _ -> failwith "Incorrect number of params")
    | _ -> failwith "Name wrapped in |"
  in
  String.split_lines s
  |> List.filter_map ~f:nonempty_line
  |> List.map ~f:game_of_line
  |> List.map ~f:(fun game -> Game.id game, game)
  |> Game_id.Map.of_alist_exn
;;

let mkpeople s =
  let open Game_attribute in
  let num_players s =
    match String.split s ~on:'-' with
    | [ lo; hi ] -> Some (Num_players [ Int.of_string lo, 4.; Int.of_string hi, 4. ])
    | _ -> None
  in
  let person_of_line line =
    let fields = Queue.of_list (String.split ~on:'\t' line) in
    let extract () = Queue.dequeue fields in
    let field parse =
      let%bind.Option field = extract () in
      let%bind.Option value = extract () in
      let%bind.Option field = parse field in
      Some (field, Float.of_string value)
    in
    let flt cons =
      field (fun s ->
          try Some (cons (Float.of_string s)) with
          | _ -> None)
    in
    let name = Queue.dequeue_exn fields in
    let id = Person_id.of_string (slugify name) in
    let filename =
      Queue.dequeue_exn fields
      |> nonempty_line
      |> Option.value_map ~f:(sprintf "people/%s") ~default:"OTYQH2b.mp4"
    in
    let length = flt length in
    let complexity = flt complexity in
    let strategy = flt strategy in
    let luck = flt luck in
    let cooperation = flt cooperation in
    let deception = flt deception in
    let unfriendly_knife_interaction = flt unfriendly_knife_interaction in
    let triviality = flt triviality in
    let artistry = flt artistry in
    let num_players = field num_players in
    (* length complexity strategy luck cooperation deception unf triv artistry *)
    { Person.id
    ; name
    ; criteria =
        List.filter_opt
          [ length
          ; complexity
          ; strategy
          ; luck
          ; cooperation
          ; deception
          ; unfriendly_knife_interaction
          ; triviality
          ; artistry
          ; num_players
          ]
    ; avatar = [ { src = filename; content_type = "video/mp4" } ]
    }
  in
  String.split_lines s
  |> List.filter_map ~f:nonempty_line
  |> List.map ~f:person_of_line
  |> List.map ~f:(fun p -> Person.id p, p)
  |> Person_id.Map.of_alist_exn
;;

let default =
  { games =
      mkgames
        (* length complexity strategy luck cooperation deception unf triv artistry *)
        {|
4.0 3.0 2.0 3.0 0.0 1.0 3.0 1.0 1.0 | Slay the Spire              | slay_the_spire.jpg   | 1 4. 2 1. 5 0.
1.0 2.0 2.0 2.0 3.0 4.0 4.0 1.0 2.0 | Among Us                    | among_us.png         | 4 1. 6 3. 10 4.
2.0 4.0 1.0 4.0 4.0 0.0 2.0 0.0 1.0 | Toaster Wars                | toaster_wars.png     | 1 4. 10 1.
4.0 4.0 4.0 0.0 3.0 1.0 0.0 0.0 4.0 | Ready Pwner One             | ready_pwner_one.jpeg | 1 3. 4 4. 20 3. 200 0.
1.0 2.0 3.0 2.0 3.0 4.0 1.0 1.0 2.0 | One Night Ultimate Werewolf | onenight.webp        | 3 1. 6 4. 8 2. 11 0.
2.0 3.0 4.0 3.0 3.0 4.0 2.0 1.0 2.0 | Secret Hitler               | secret_hitler.png    | 3 1. 8 4. 10 3.
2.0 2.0 3.0 3.0 1.0 1.0 2.0 1.0 1.0 | Dominion                    | dominion.jpg         | 2 3. 4 4.
2.0 1.0 1.0 1.0 2.0 2.0 0.0 2.0 4.0 | skribbl.io                  | skribblio.png        | 3 3. 4 4. 6 4. 8 1. 12 0.
1.0 1.0 3.0 1.0 4.0 0.0 0.0 3.0 2.0 | Person Do Thing             | person_do_thing.png  | 2 2. 3 4. 5 4. 10 0.
2.0 2.0 4.0 3.0 4.0 1.0 4.0 0.0 1.0 | Hanabi                      | hanabi.jpg           | 3 3. 4 4. 5 4.
4.0 3.0 4.0 0.0 3.0 0.0 0.0 1.0 3.0 | Baba is You                 | baba_is_you.jpg      | 1 3.5 2 4. 5 2. 10 0.
3.0 3.0 4.0 0.0 0.0 2.0 0.0 1.0 1.0 | The Watness                 | the_watness.png      | 1 4. 2 2. 10 0.
2.0 1.0 2.0 3.0 2.0 1.0 0.0 3.0 4.0 | Drawful                     | drawful.jpeg         | 2 2. 5 4. 8 4. 10 0.
4.0 1.0 1.0 3.0 3.0 1.0 0.0 3.0 2.0 | Animal Crossing             | animal_crossing.jpg  | 1 3. 2 4. 5 4. 10 0. 
3.0 4.0 2.0 2.0 3.0 1.0 2.0 1.0 3.0 | Pwn Adventure               | pwn_adventure.png    | 1 3.5 2 4. 4 2.
2.0 2.0 4.0 3.0 3.0 4.0 4.0 1.0 2.0 | Coup                        | coup.jpg             | 2 1. 3 3. 4 4. 7 3.
2.0 0.0 0.0 4.0 0.0 0.0 4.0 4.0 0.0 | War                         | war.jpg              | 2 4.
|}
  ; people =
      mkpeople
        {|
strikeskids	strikeskids.mp4	4	1	3	2	3	4	1	4	4	2			2	0.5	0	3	2	1	3-5	3
bluepichu	bluepichu.mp4	2.5	2	3	2.5	3	4	2	2	2	1	2	1	2	1.5	0	4	3	2	4-8	3.5
zwad3	zwad3.mp4	2	4	4	1	3	2	4	1	4	3	4	3	1	1	1	3				
zaratec	zaratec.mp4	2	1	3	2	1	2	3	3	2	5	4	5	4	5	0	1	2	1	2-5	2
f0xtr0t	f0xtr0t.mp4	3	2	3	2	3	2	1	4	3	1	3	1	3	2	0	4	4	2	3-6	3
tylerni7	tylerni7.mp4	4	2	4	2	4	4	1	2	2	2	4	3	1	2	0	2	3	3	3-7	2
panda		3	3	2	3	2	3	0	5	2	5	3	3	2	3	1	3	3	2		
clam	clam.mp4	2	1	2	2	1	2	4	2	3	1	2	2	3	1	1	2	3	3		
luke	luke.mp4	3	2	4	3	4	4	1	4	2	2	4	4	1	3	1	4	4	3	5-8	4
kylar	kylar.mp4	2	1	4	2	4	3	2	1	3	3	3	4	1	2	0	4	1	4		
ubuntor	ubuntor.mp4	4	3	4	3	2	1	2	1	4	2	0	5	1	1	1	1	3	1		
b2xiao	b2xiao.mp4	2	3	3	3	4	2	1	4	3	2	2	1	0	5	0	5	0	3	1-5	1
|}
  ; rooms =
      List.range ~stop:`inclusive 1 4
      |> List.map ~f:(fun id -> Room_id.of_string (Int.to_string id))
      |> Room_id.Set.of_list
  }
;;
