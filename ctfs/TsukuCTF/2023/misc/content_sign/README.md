misc medium

どうやら、この画像には署名技術を使っているらしい。この署名技術は、画像に対しての編集を記録することができるらしい。署名技術を特定し、改変前の画像を復元してほしい。 Flag形式はTsukuCTF23{<一個前に署名した人の名前>&<署名した時刻(ISO8601拡張形式)>}です。例えば、一個前に署名した人の名前は「Tsuku」で、署名した時刻が2023/12/09 12:34:56(GMT+0)の場合、フラグはTsukuCTF23{Tsuku&2023-12-09T12:34:45+00:00}です。なお、タイムゾーンはGMT+0を使用してください。

It seems this image is applied digital signature, which can record edit history for an image.
Identify the technology and restore the raw image, which means the image before revised.

The flag format is TsukuCTF23{<the name of the previous signing person>&<signed time(ISO8601 extended format)>}
