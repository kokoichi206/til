let greet who =
  let open Tyxml.Html in
  html
    (head (title (txt "Greeting")) [])
    (body [ h1 [ txt "Good morning, "; txt who; txt "!" ] ])

let html_to_string html = Format.asprintf "%a" (Tyxml.Html.pp ()) html
let elt_to_string elt = Fmt.str "%a" (Tyxml.Html.pp_elt ()) elt

let res2 =
  let open Tyxml in
  let ocaml = Html.(div ~a:[ a_class [ "ocaml" ] ] [ txt "OCaml" ]) in
  Dream.html @@ elt_to_string ocaml

let run =
  let port = 12334 in
  Dream.run ~port @@ Dream.logger
  @@ Dream.router
       [
         Dream.get "/" (fun _ -> Dream.html "Hello, Dream!");
         Dream.get "/hello/:name" (fun req ->
             let name = Dream.param req "name" in
             Dream.html ("Hello, " ^ name ^ "!"));
         Dream.post "/echo" (fun req ->
             let open Lwt.Syntax in
             (* body is async...? *)
             (* This expression has type string Lwt.t but an expression was expected of type stringocamllsp *)
             let* body = Dream.body req in
             Printf.printf "Received body: %s\n" body;
             Dream.respond
               ~headers:[ ("Content-Type", "application/octet-stream") ]
               body)
         (*  https://github.com/aantron/dream/tree/master/example/w-tyxml#files *);
         Dream.get "/:word" (fun _ ->
             Dream.html (html_to_string (greet "world")));
         Dream.get "/ocaml" (fun _ -> res2);
       ]
