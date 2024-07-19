let () = print_endline "Hello, PIYOPIYO!"
let () = Printf.printf "%s\n" "pifaaaeafa"

(* import module (every file defines a module) *)
let () = Printf.printf "%s\n" Hello.En.v

let () = 
  let result = Add.add_one 1 in
  Printf.printf "Result %d\n" result

(* let () = 
  Hello.Hclient.download *)

let () =
  let n = 10 in
  let fact = Hello.Hof.fact n in
  Printf.printf "Fact %d: %d\n" n fact
  (* Hello.Hof.fibs 10 |> List.iter (Printf.printf "%d\n") *)
