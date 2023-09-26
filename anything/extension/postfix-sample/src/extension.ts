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
  let disposable = vscode.commands.registerCommand(
    "extension.consoleCommand",
    (arg1: string, arg2: vscode.Position) => {
      const words = arg1.split(".");
      const text = words.slice(0, -1).join(".");

      const editor = vscode.window.activeTextEditor;

      const { whitespace, variable } = extractWhitespaceAndText(text);

      if (editor) {
        editor.edit((editBuilder) => {
          const startPosition = new vscode.Position(
            arg2.line,
            arg2.character - arg1.length
          );
          const endPosition = new vscode.Position(
            arg2.line,
            arg2.character + arg1.length
          );
          const replaceRange = new vscode.Range(startPosition, endPosition);

          editBuilder.replace(
            replaceRange,
            `${whitespace}// eslint-disable-next-line no-console\n${whitespace}console.log('${variable}: ' + ${variable});`
          );
        });
      }
    }
  );

  context.subscriptions.push(disposable);

  const provider1 = vscode.languages.registerCompletionItemProvider(
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
      {
        language: "vue",
        scheme: "file",
      },
    ],
    {
      provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
      ) {
        const commitCharacterCompletion = new vscode.CompletionItem("console");
        commitCharacterCompletion.commitCharacters = ["."];
        commitCharacterCompletion.documentation = new vscode.MarkdownString(
          `console.log("VAR: " + VAR) with no lint`
        );

        const lineText = document.lineAt(position).text;
        const linePrefix = lineText.substring(0, position.character);

        commitCharacterCompletion.command = {
          title: "Sample Command",
          command: "extension.consoleCommand", // このコマンドは事前に定義されている必要があります
          arguments: [linePrefix, position], // 必要に応じて引数を渡すことができます
        };

        return [commitCharacterCompletion];
      },
    }
  );

  context.subscriptions.push(provider1);
}
