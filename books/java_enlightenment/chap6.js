let myObject = {
    func1: function() {
        console.log(this);
        let func2 = function() {
            console.log(this);
            let func3 = function () {
                console.log(this);
            }();
        }();
    }
}

myObject.func1();
