function squareOf(n: number) {
  return n * n
}
squareOf(2)
// squareOf("z") // Shows error

let c: {
  firstName: string
  lastName: string
} = {
  firstName: 'john',
  lastName: 'barrowman'
}

console.log(c.firstName)

class Person {
  constructor(
    // public is shorthand for this.blahblah
    public firstName: string,
    public lastName: string
  ) {}
}
c = new Person('matt', 'smith')

