/**
 * Binary Trees
 */
 type TreeNode = {
  value: string
}
type LeafNode = TreeNode & {
  isLeaf: true
}
type InnerNode = TreeNode & {
  children: [TreeNode] | [TreeNode, TreeNode]
}

let a: TreeNode = {value: 'a'}
let b: LeafNode = {value: 'b', isLeaf: true}
let c: InnerNode = {value: 'c', children: [b]}

let a1 = mapNode(a, _ => _.toUpperCase())
let b1 = mapNode(b, _ => _.toUpperCase())
let c1 = mapNode(c, _ => _.toUpperCase())

// T has an upper bound of TreeNode.
// That is, T can be either a TreeNode or a subtype of TreeNode.
function mapNode<T extends TreeNode>(
  node: T,
  f: (value: string) => string
): T {
  return {
    ...node,
    value: f(node.value)
  }
}


// Bounded polymorphism with multiple constraints
type HasSides = {numberOfSides: number}
type SidesHaveLength = {sideLength: number}

function logPermiter<
  Shape extends HasSides & SidesHaveLength
>(s: Shape): Shape {
  console.log(s.numberOfSides * s.sideLength)
  return s
}

type Square = HasSides & SidesHaveLength
let square: Square = {numberOfSides: 4, sideLength: 3}
logPermiter(square)


// Using bounded polymorphism to model arity

// function call(
//   f: (...args: unknown[]) => unknown,
//   ...args: unknown[]
// ): unknown {
//   return f(...args)
// }

function call<T extends unknown[], R>(
  f: (...args: T) => R,
  ...args: T
): R {
  return f(...args)
}

function fill(length: number, value: string): string[] {
  return Array.from({length}, () => value)
}

console.log(call(fill, 10, 'a'))
