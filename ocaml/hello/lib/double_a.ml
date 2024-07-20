let square  x = x * x
let add_one x = x + 1

let one = 5 |> square |> add_one
let two = add_one @@ square 5

let () = 
  Printf.printf "\n\none: %d\n" one
let () =
  Printf.printf "two: %d\n" two
