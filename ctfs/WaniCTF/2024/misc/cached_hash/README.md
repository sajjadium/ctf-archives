If you add sensitive information to a container image, it seems that it will remain in the intermediate layers even if you delete it later.

But we’re using multi-stage builds this time, so it should be okay, right?

コンテナイメージに機密情報を追加すると、あとから削除しても途中のレイヤーに残ってしまうらしい。

今回はマルチステージビルドを使ってるから大丈夫だよね……？

Writer : ciffelia
