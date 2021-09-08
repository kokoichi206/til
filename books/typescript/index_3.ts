let set = new Set
set.add(1).add(2).add(3)
console.log(set.has(2))

// class Set {
//   has(value: number): boolean {}
//   add(value: number): this {}   // this !!
// }
// // Now, you can remove the add override from MutableSet
// // This is a really convenient feature for working with chained APIs
// class MutableSet extends Set {
//   delete(value: number): boolean {}
// }


/**
 * Interfaces
 */

// type alias
// type Food = {
//   calories: number
//   tasty: boolean
// }
// type Sushi = Food & {
//   salty: boolean
// }
// type Cake = Food & {
//   sweet: boolean
// }

// interface
interface Food {
  calories: number
  tasty: boolean
}
interface Sushi extends Food {
  salty: boolean
}
interface Cake extends Food {
  sweet: boolean
}


interface Animal {
  eat(food: string): void
  sleep(hours: number): void
}

class Cat implements Animal {
  eat(food: string) {
    console.info('Ate some', food, '. Mmm!')
  }
  sleep(hours: number) {
    console.info('slept for', hours, 'hours')
  }
}
