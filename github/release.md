```sh
# 例が master なの良くないな
curl \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/releases \
  -d '{"tag_name":"v1.0.0","target_commitish":"master","name":"v1.0.0","body":"Description of the release","draft":false,"prerelease":false,"generate_release_notes":false}'

curl -X POST -H "Accept: application/vnd.github+json" https://api.github.com/repos/kokoichi206/til/releases -d '{"tag_name":"v1.0.0","target_commitish":"main","name":"v1.0.0","body":"Description of the release","draft":false,"prerelease":false,"generate_release_notes":false}'

curl -X POST -H "Accept: application/vnd.github+json" -H "Authorization: token ${TOKEN_WITH_REPO}" https://api.github.com/repos/kokoichi206/til/releases -d '{"tag_name":"v1.0.0","target_commitish":"main","name":"v1.0.0","body":"Description of the release","draft":false,"prerelease":false,"generate_release_notes":false}'
```

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

## 統計情報

- [キャッシングについて](https://docs.github.com/ja/rest/metrics/statistics#a-word-about-caching)
  - 202 の時はしばらく経ってからリトリアする、回復したら 200 になるはず

```sh
curl -H "Accept: application/vnd.github+json" -H "Authorization: token ${TOKEN_WITH_REPO}" https://api.github.com/repos/kokoichi206/til/stats/commit_activity

curl -H "Accept: application/vnd.github+json" -H "Authorization: token ${TOKEN_WITH_REPO}" https://api.github.com/repos/kokoichi206/til/stats/code_frequency


"https://api.github.com/repos/${{ secrets.USER_NAME }}/@/stats/code_frequency"


curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/stats/commit_activity
```
