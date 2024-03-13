## [Top Architecture Blog Posts of 2023](https://aws.amazon.com/jp/blogs/architecture/top-architecture-blog-posts-of-2023/)

- Textract
  - https://aws.amazon.com/jp/textract/pricing/
  - OCR だけみたいな使い方もできる
  - 非同期実行のパターンであれば、複数ページの pdf も可能そう？
    - https://dev.classmethod.jp/articles/reintro-managed-ml-textract/

### serverless

- components
  - https://aws.amazon.com/jp/serverless/
- coca-cola
  - https://aws.amazon.com/jp/solutions/case-studies/coca-cola-freestyle/
  - API Gateway websocket api

## [Best practices for implementing event-driven architectures in your organization](https://aws.amazon.com/jp/blogs/architecture/best-practices-for-implementing-event-driven-architectures-in-your-organization/)

- SNS
  - ファンアウト
- SQS
  - **標準キューでは at-least once**
    - FIFO キューにすると Exactly Once を実現できる
- Lambda
  - 3 invocation models
    - Synchronous
      - API Gateway, ...
    - Asynchronous
      - SNS, S3, ...
    - Poll based
      - SQS, Kinesis, ...
      - lambda サービスがロングポーリングする

### Links

- [【AWS】SQSキューの前には難しいこと考えずにSNSトピックを挟むと良いよ、という話](https://dev.classmethod.jp/articles/sns-topic-should-be-placed-behind-sqs-queue/)
- [RECRUIT: AWS研修　Amazon SNSとAmazon SQS](https://speakerdeck.com/recruitengineers/awsyan-xiu-amazon-snstoamazon-sqs?slide=10)
