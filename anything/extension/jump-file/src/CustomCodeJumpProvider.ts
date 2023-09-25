import * as vscode from "vscode";

export class CustomCodeJumpProvider implements vscode.DefinitionProvider {
  provideDefinition(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken
  ): vscode.ProviderResult<vscode.Definition | vscode.LocationLink[]> {
    const targetText = document.getText();
    const editor = vscode.window.activeTextEditor;

    const selection = document.getWordRangeAtPosition(
      editor?.selection.active ?? new vscode.Position(0, 0)
    );
    const selectedText = document.getText(selection);

    this.jumpFile(selectedText);
    return;
  }

  private jumpFile(selectedText: string): void {
    const parts = selectedText.split("-");

    const capitalize = (str: string) =>
      str.charAt(0).toUpperCase() + str.slice(1);
    const componentName = parts[0];
    const folderName = parts.slice(1).map(capitalize).join("");
    vscode.workspace
      .findFiles(`**/*.vue`, "**/node_modules/**")
      .then((value) => {
        value.forEach((v) => {
          const path = v.path;
          if (path.includes(componentName) && path.includes(folderName)) {
            vscode.workspace.openTextDocument(v).then((doc) => {
              vscode.window.showTextDocument(doc, { preview: false });
            });
          }
        });
      });
  }
}
