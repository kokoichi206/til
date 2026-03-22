``` sh
rebar3 new lib pbt

rebar3 help proper

❯ rebar3 new proper foundations
===> Writing test/prop_foundations.erl
```

## rebar.config の project_plugins vs deps

- `deps`: アプリの実行時依存。ビルド成果物に含まれる
- `project_plugins`: rebar3 自体を拡張するプラグイン。サブコマンドの追加等に使う
  - `_build/default/plugins/` に配置される
  - `init/1` で `providers:create/1` を呼んでコマンドを登録する仕組み

```erlang
%% rebar3 に "proper" サブコマンドを追加
{project_plugins, [rebar3_proper]}.

%% test プロファイル時のみ proper ライブラリを依存に追加
{profiles, [{test, [{deps, [proper]}]}]}.
```

`rebar3 proper` 実行時は test/ 配下の `prop_*.erl` を探し、その中の `prop_*()` 関数を自動検出して `proper:quickcheck/2` で実行する。
