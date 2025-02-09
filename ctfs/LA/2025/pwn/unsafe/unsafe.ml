let vuln arr size =
  let rec get_data i = 
    print_endline "input index-value pairs please";
    let index = read_int () in
    let value = read_int () in
      match i with
      | 0 -> ()
      | 10 -> Array.unsafe_set arr index value; get_data (i-1)
      | _ -> Array.set arr index value; get_data (i-1)
    in
  get_data size;
  print_endline "leggo"

let leak arr =
  print_endline "leak where";
  let index = read_int () in
  Array.unsafe_get arr index

let main () =
  let arr = Array.make 5 0 in
  print_endline "are you readyyy";
  print_endline ("leakk 1: " ^ string_of_int (leak arr));
  print_endline ("leakk 2: " ^ string_of_int (leak arr));
  vuln arr 10;
  print_endline "i wonder if you won"

let () = main ()