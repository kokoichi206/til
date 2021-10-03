const { ApolloServer, gql } = require('apollo-server');

// GraphQLスキーマ作成
const typeDefs = gql`
  type Query {
    allBooks: [Book]
    getBook(isbn: String!): Book
  }
  type Book {
    title: String
    author: String
    year: Int!
    isbn: String!
  }
`;

//
// データソースとリゾルバの定義
// ハードコーディングしている
// 実際の開発ではDBやドメインロジックを実装
//
const books = [
  {
    title: 'Webを支える技術　HTTP, URI, HTML',
    author: 'Yamamoto',
    year: 2010,
    isbn: "978-4-7741-4201-3",
  },
  {
    title: '失敗から学ぶRDBの正しい歩き方',
    author: 'Sone',
    year: 2019,
    isbn: "978-4-1156-4201-3",
  },
  {
    title: 'Vue.js入門 基礎から実践アプリ',
    author: 'katayama',
    year: 2018,
    isbn: "978-4-7777-4201-3",
  },
];

const resolvers = {
  Query: {
    allBooks: () => books,
    getBook: (_, args) => books.find(b.isbn === args.isbn),
  },
};

// Apollo Serverインスタンスの作成
const server = new ApolloServer({
  typeDefs,
  resolvers,

  // コンテキストを追加する場合
  context: (({ req }) => {
    // リクエストヘッダのAuthorizationの値を取得する
    const token = req.headers.authorization || '';
    const user = getUser(token);
    return {user}
  })
});


server.listen().then(({ url }) => {
  console.log(`Server ready at ${url}`);
});

