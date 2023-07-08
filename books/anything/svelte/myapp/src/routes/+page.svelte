<script>
    import Child from "$lib/components/Child.svelte";

    let text = "text, txt"
    let html = "1<br/>2"
    let arr = [
        {
            link: "#1",
            text: "text1"
        },
        {
            link: "#2",
            text: "text2"
        }
    ]
    let obj = {
        imgpath: "https://placehold.jp/150x150.png",
        text: "text"
    }
</script>

<Child {text} {html} {arr} {obj} />

<h1>Welcome {message} from {prefix} </h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
