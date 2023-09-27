- [Your First Extension](https://code.visualstudio.com/api/get-started/your-first-extension)
  - [Hello World ができない](https://zenn.dev/b7472/articles/dbe2fba3125b1c)
- [how to override the default definition](https://github.com/microsoft/vscode/issues/76231)
- [vscode-extension-samples](https://github.com/microsoft/vscode-extension-samples)
- [virtual documents](https://code.visualstudio.com/api/extension-guides/virtual-documents)
- [Activation Events](https://code.visualstudio.com/api/references/activation-events#onFileSystem)

## Compile

`.vsix` ファイルにして配布

``` sh
npx vsce package
```

## Install

Download the `.vsix` file.

Command + P > Extension: Install From VSIX
