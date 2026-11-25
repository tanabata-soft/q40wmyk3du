"""作品の曲設定（NK-S011）。

単位D（生成器一本化）: 生成器本体の正はテンプレート repo
（mmishina-art/digitalcd-engine）の scripts/chartgen/ パッケージ1か所。
作品側はこの SONGS メタデータと歌詞入力（src/game/data/lyrics.json）だけを
持ち、scripts/generate-charts.py（入口ブートストラップ）がテンプレートの
chartgen を参照して生成する。曲を足すときはここに1曲分を足す。
各キーの意味はテンプレート scripts/chartgen/config.py のコメント参照。
"""

SONGS = {
    # NK-S011『青い火よ、消えないで ―サウンド単行本エンドロールソングス―』の収録曲。
    # 音源は src/game/assets/track0N.mp3（唯一の正規音源 MP3 192kbps。
    # CD 側プレイヤーも同じ音源を共有する）。FEVER（サビ）区間と方針は
    # v1.0.1 までの生成器（v6-4）の SONGS メタデータをそのまま引き継ぐ。
    "aoibi": {
        "title": "青い火よ、消えないで",
        "audio": "src/game/assets/track01.mp3",
        "fever": [[0.9, 19.5], [78.7, 97.5]],
        "chart_v5": True,
        "chorus_layer": "vocal",
        "chorus_bonus": 0.5,
        "flick": True,
        # v6-5: バラードプロファイルは実測分類で対象外（detect スコア4）のため
        # 明示的に OFF（2026-11-25 標準引き上げ時に実測）
        "ballad": False,
    },
    "yonbyo": {
        "title": "四秒だけ連れていく",
        "audio": "src/game/assets/track02.mp3",
        "fever": [[47.3, 75.5], [120.0, 147.5], [164.6, 189.5]],
        "chart_v5": True,
        "chorus_layer": "vocal",
        "chorus_bonus": 0.5,
        "flick": True,
        # v6-5: バラード判定は detect_ballad でスコア3（OFF）だが、本曲は
        # SF Ballad で easy のボーカル被覆の空白が本作中最悪（自動判定の生成で
        # unfilledGaps=6・最大3,808ms）のため、NK-S009『あなた』の先例に倣い
        # 明示的に True でピン留めする（2026-11-25 標準引き上げ時に実測比較）
        "ballad": True,
        # フリック固定: 公開済み（v1.0.1）譜面から導出した現行フリック
        # [時刻ms, レーン, ランク]（ランク: easy から出る=0／normal から=1／
        # hard のみ=2）。バラード化で密度計画が変わってもフリックは動かない
        "flick_lock": [[21060,1,0],[47331,2,1],[48762,2,2],[62299,3,0],[65109,2,1],[66804,2,2],[74141,0,0],[93298,1,0],[125388,2,0],[128197,2,1],[129892,2,2],[146727,1,0],[164666,0,0],[178910,0,0],[182145,0,1]],
    },
    "anzen": {
        "title": "安全運転で、またどうぞ",
        "audio": "src/game/assets/track03.mp3",
        "fever": [[34.6, 55.5], [103.8, 122.0]],
        "chart_v5": True,
        "chorus_layer": "vocal",
        "chorus_bonus": 0.5,
        "flick": True,
        # v6-5: バラードプロファイルは実測分類で対象外（detect スコア4）のため
        # 明示的に OFF（2026-11-25 標準引き上げ時に実測）
        "ballad": False,
    },
}
