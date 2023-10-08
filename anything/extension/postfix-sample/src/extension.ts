import * as vscode from "vscode";

const whiteSpaceTrimmer = /^(\s*)(\S.*)$/;

function extractWhitespaceAndText(input: string): {
  whitespace: string;
  variable: string;
} {
  const match = input.match(whiteSpaceTrimmer);
  if (match) {
    return {
      whitespace: match[1], // 先頭の空白
      variable: match[2], // それ以降の文字列
    };
  }
  return { whitespace: "", variable: "" };
}

export function activate(context: vscode.ExtensionContext) {
  // const provider1 = vscode.languages.registerCompletionItemProvider(
  //   [
  //     {
  //       language: "javascript",
  //       scheme: "file",
  //     },
  //     {
  //       language: "javascript",
  //       scheme: "untitled",
  //     },
  //     {
  //       language: "typescript",
  //       scheme: "file",
  //     },
  //     {
  //       language: "typescript",
  //       scheme: "untitled",
  //     },
  //     {
  //       language: "vue",
  //       scheme: "file",
  //     },
  //   ],
  //   {
  //     provideCompletionItems(
  //       document: vscode.TextDocument,
  //       position: vscode.Position,
  //       token: vscode.CancellationToken,
  //       context: vscode.CompletionContext
  //     ) {
  //       console.log("provideCompletionItems of provider1");
  //       const commitCharacterCompletion = new vscode.CompletionItem("console");
  //       commitCharacterCompletion.commitCharacters = ["."];
  //       commitCharacterCompletion.documentation = new vscode.MarkdownString(
  //         `console.log("VAR: " + VAR) with no lint`
  //       );

  //       const lineText = document.lineAt(position).text;
  //       const linePrefix = lineText.substring(0, position.character);

  //       commitCharacterCompletion.command = {
  //         title: "Sample Command",
  //         command: "extension.consoleCommand", // このコマンドは事前に定義されている必要があります
  //         arguments: [linePrefix, position], // 必要に応じて引数を渡すことができます
  //       };

  //       return [commitCharacterCompletion];
  //     },
  //   },
  //   "."
  // );

  // context.subscriptions.push(provider1);

  const provider2 = vscode.languages.registerCompletionItemProvider(
    [
      {
        language: "javascript",
        scheme: "file",
      },
      {
        language: "javascript",
        scheme: "untitled",
      },
      {
        language: "typescript",
        scheme: "file",
      },
      {
        language: "typescript",
        scheme: "untitled",
      },
    ],
    {
      provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
      ) {
        console.log("provideCompletionItems");
        let line = document.lineAt(position.line);
        let dotIdx = line.text.lastIndexOf(".", position.character);
        if (dotIdx === -1) {
          return [];
        }

        let commentIndex = line.text.indexOf("//");
        if (commentIndex >= 0 && position.character > commentIndex) {
          return [];
        }

        let code = line.text.substring(
          line.firstNonWhitespaceCharacterIndex,
          dotIdx
        );
        let escapedCode = code.replace(/"/g, '\\"');

        // len
        let lengthSnippet = new vscode.CompletionItem("len");
        lengthSnippet.additionalTextEdits = [
          vscode.TextEdit.delete(
            new vscode.Range(
              position.translate(0, -(escapedCode.length + 1)),
              position
            )
          ),
        ];
        lengthSnippet.insertText = new vscode.SnippetString(`len(${code})`);
        lengthSnippet.kind = vscode.CompletionItemKind.Snippet;
        lengthSnippet.sortText = "\u0000";
        lengthSnippet.preselect = true;

        return [lengthSnippet];
      },
    },
    "."
  );

  context.subscriptions.push(provider2);
}
