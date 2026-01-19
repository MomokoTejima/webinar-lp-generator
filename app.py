import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="ウェビナーLP生成",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ウェビナーLP自動生成")
st.write("情報を入力するだけで、公開可能なLPを自動生成します")

# サイドバーで基本設定
st.sidebar.header("🎨 デザイン設定")
primary_color = st.sidebar.color_picker("メインカラー", "#4F46E5")

# メインエリア
tab1, tab2, tab3 = st.tabs(["📝 基本情報", "👥 登壇者・内容", "📄 生成・公開"])

# セッションステートの初期化
if 'speakers' not in st.session_state:
    st.session_state.speakers = [{"name": "", "company": "", "role": "", "bio": "", "image": ""}]
if 'contents' not in st.session_state:
    st.session_state.contents = [{"title": "", "description": ""}]
if 'timetable' not in st.session_state:
    st.session_state.timetable = [{"time": "", "content": ""}]
if 'targets' not in st.session_state:
    st.session_state.targets = [""]

with tab1:
    st.subheader("ウェビナー基本情報")

    col1, col2 = st.columns(2)

    with col1:
        webinar_title = st.text_input("ウェビナータイトル *", placeholder="例：要件定義と開発を進化させる生成AIの実践活用")
        event_label = st.text_input("ラベル", value="無料ウェビナー", placeholder="例：無料ウェビナー")
        event_date = st.text_input("開催日 *", placeholder="例：2025年9月30日（火）")
        event_time = st.text_input("開催時間 *", placeholder="例：12:00〜13:00")

    with col2:
        event_format = st.text_input("開催形式", value="オンライン（Zoom）", placeholder="例：オンライン（Zoom）")
        event_price = st.text_input("参加費", value="無料", placeholder="例：無料")
        cta_url = st.text_input("申し込みURL *", placeholder="例：https://forms.gle/xxxxx")
        meta_description = st.text_input("ページ説明（SEO用）", placeholder="例：生成AI×プロダクト開発の進化...")

    st.divider()

    st.subheader("概要説明文")
    description_text = st.text_area(
        "ウェビナーの説明文",
        height=200,
        placeholder="""例：
生成AIは、もはやPoC止まりの技術ではありません。
実務にどう組み込み、開発現場でどう成果を出すのか──そのリアルを、
プロダクトマネージャーとエンジニア視点で体感できる60分。"""
    )

    st.divider()

    st.subheader("会社情報")
    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("自社名", placeholder="例：株式会社パンハウス")
        logo_url = st.text_input("自社ロゴURL", placeholder="例：https://example.com/logo.png")

    with col2:
        partner_name = st.text_input("共催会社名（任意）", placeholder="例：株式会社ROUTE06")
        partner_logo_url = st.text_input("共催会社ロゴURL（任意）", placeholder="例：https://example.com/partner-logo.png")

    copyright_text = st.text_input("コピーライト", value=f"© {datetime.now().year} {company_name or '会社名'} All Rights Reserved.")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 登壇者")

        for i, speaker in enumerate(st.session_state.speakers):
            with st.expander(f"登壇者 {i+1}", expanded=(i==0)):
                st.session_state.speakers[i]["name"] = st.text_input(f"氏名", key=f"sp_name_{i}", value=speaker.get("name", ""))
                st.session_state.speakers[i]["company"] = st.text_input(f"会社名", key=f"sp_company_{i}", value=speaker.get("company", ""))
                st.session_state.speakers[i]["role"] = st.text_input(f"役職", key=f"sp_role_{i}", value=speaker.get("role", ""))
                st.session_state.speakers[i]["image"] = st.text_input(f"写真URL", key=f"sp_image_{i}", value=speaker.get("image", ""))
                st.session_state.speakers[i]["bio"] = st.text_area(f"プロフィール", key=f"sp_bio_{i}", value=speaker.get("bio", ""), height=100)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("＋ 登壇者を追加"):
                st.session_state.speakers.append({"name": "", "company": "", "role": "", "bio": "", "image": ""})
                st.rerun()
        with col_b:
            if len(st.session_state.speakers) > 1 and st.button("－ 最後を削除"):
                st.session_state.speakers.pop()
                st.rerun()

    with col2:
        st.subheader("📋 登壇内容")

        for i, content in enumerate(st.session_state.contents):
            with st.expander(f"セッション {i+1}", expanded=(i==0)):
                st.session_state.contents[i]["title"] = st.text_input(f"タイトル", key=f"ct_title_{i}", value=content.get("title", ""))
                st.session_state.contents[i]["description"] = st.text_area(f"説明", key=f"ct_desc_{i}", value=content.get("description", ""), height=100)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("＋ セッションを追加"):
                st.session_state.contents.append({"title": "", "description": ""})
                st.rerun()
        with col_b:
            if len(st.session_state.contents) > 1 and st.button("－ 最後を削除", key="del_content"):
                st.session_state.contents.pop()
                st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏰ タイムテーブル")

        for i, item in enumerate(st.session_state.timetable):
            col_t, col_c = st.columns([1, 3])
            with col_t:
                st.session_state.timetable[i]["time"] = st.text_input(f"時間", key=f"tt_time_{i}", value=item.get("time", ""), placeholder="12:00")
            with col_c:
                st.session_state.timetable[i]["content"] = st.text_input(f"内容", key=f"tt_content_{i}", value=item.get("content", ""), placeholder="オープニング")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("＋ 行を追加"):
                st.session_state.timetable.append({"time": "", "content": ""})
                st.rerun()
        with col_b:
            if len(st.session_state.timetable) > 1 and st.button("－ 最後を削除", key="del_tt"):
                st.session_state.timetable.pop()
                st.rerun()

    with col2:
        st.subheader("🎯 対象者")

        for i, target in enumerate(st.session_state.targets):
            st.session_state.targets[i] = st.text_input(f"対象 {i+1}", key=f"target_{i}", value=target, placeholder="例：生成AIを業務に活用したい方")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("＋ 対象を追加"):
                st.session_state.targets.append("")
                st.rerun()
        with col_b:
            if len(st.session_state.targets) > 1 and st.button("－ 最後を削除", key="del_target"):
                st.session_state.targets.pop()
                st.rerun()

    st.divider()

    st.subheader("📢 CTA（申し込みセクション）")
    col1, col2 = st.columns(2)
    with col1:
        cta_title = st.text_input("CTAタイトル", value="参加申し込み受付中", placeholder="例：参加申し込み受付中")
    with col2:
        cta_subtitle = st.text_input("CTAサブテキスト", value="お席に限りがございます。お早めにお申し込みください。")

with tab3:
    st.subheader("HTMLを生成")

    if st.button("🔨 LPを生成する", type="primary", use_container_width=True):
        # バリデーション
        if not webinar_title:
            st.error("ウェビナータイトルを入力してください")
        elif not cta_url:
            st.error("申し込みURLを入力してください")
        else:
            # テンプレートを読み込み
            template_path = os.path.join(os.path.dirname(__file__), "templates", "webinar_lp.html")

            with open(template_path, "r", encoding="utf-8") as f:
                html_template = f.read()

            # 登壇者HTMLを生成
            speakers_html = ""
            for speaker in st.session_state.speakers:
                if speaker.get("name"):
                    speakers_html += f'''
      <div class="speaker-card">
        <img src="{speaker.get('image', 'https://via.placeholder.com/120')}" alt="{speaker['name']}" class="speaker-image">
        <p class="speaker-company">{speaker.get('company', '')}</p>
        <h3 class="speaker-name">{speaker['name']}</h3>
        <p class="speaker-role">{speaker.get('role', '')}</p>
        <p class="speaker-bio">{speaker.get('bio', '')}</p>
      </div>'''

            # 登壇内容HTMLを生成
            contents_html = ""
            for i, content in enumerate(st.session_state.contents):
                if content.get("title"):
                    contents_html += f'''
      <div class="content-item">
        <div class="content-number">{i+1}</div>
        <div class="content-body">
          <h3>{content['title']}</h3>
          <p>{content.get('description', '')}</p>
        </div>
      </div>'''

            # タイムテーブルHTMLを生成
            timetable_html = ""
            for item in st.session_state.timetable:
                if item.get("time") and item.get("content"):
                    timetable_html += f'''
        <tr>
          <td class="time">{item['time']}</td>
          <td>{item['content']}</td>
        </tr>'''

            # 対象者HTMLを生成
            targets_html = ""
            for target in st.session_state.targets:
                if target:
                    targets_html += f'''
      <div class="target-item">
        <div class="target-icon">&#10003;</div>
        <span>{target}</span>
      </div>'''

            # パートナーロゴHTML
            partner_logo_html = ""
            if partner_logo_url:
                partner_logo_html = f'<img src="{partner_logo_url}" alt="{partner_name}">'

            # テンプレートの置換
            html_output = html_template

            # 基本情報
            html_output = html_output.replace("{{webinar_title}}", webinar_title or "")
            html_output = html_output.replace("{{meta_description}}", meta_description or "")
            html_output = html_output.replace("{{event_label}}", event_label or "")
            html_output = html_output.replace("{{event_date}}", event_date or "")
            html_output = html_output.replace("{{event_time}}", event_time or "")
            html_output = html_output.replace("{{event_format}}", event_format or "")
            html_output = html_output.replace("{{event_price}}", event_price or "")
            html_output = html_output.replace("{{cta_url}}", cta_url or "#")
            html_output = html_output.replace("{{description_text}}", description_text or "")

            # 会社情報
            html_output = html_output.replace("{{company_name}}", company_name or "")
            html_output = html_output.replace("{{logo_url}}", logo_url or "https://via.placeholder.com/150x40")
            html_output = html_output.replace("{{partner_name}}", partner_name or "")
            html_output = html_output.replace("{{partner_logo_url}}", partner_logo_url or "")
            html_output = html_output.replace("{{copyright}}", copyright_text or "")

            # CTA
            html_output = html_output.replace("{{cta_title}}", cta_title or "参加申し込み受付中")
            html_output = html_output.replace("{{cta_subtitle}}", cta_subtitle or "")

            # カラー
            html_output = html_output.replace("{{primary_color}}", primary_color)

            # 条件分岐の処理
            if partner_logo_url:
                html_output = html_output.replace("{{#if partner_logo_url}}", "")
                html_output = html_output.replace("{{/if}}", "")
            else:
                import re
                html_output = re.sub(r'\{\{#if partner_logo_url\}\}.*?\{\{/if\}\}', '', html_output, flags=re.DOTALL)

            # 配列データの置換
            html_output = re.sub(
                r'\{\{#each speakers\}\}.*?\{\{/each\}\}',
                speakers_html,
                html_output,
                flags=re.DOTALL
            )
            html_output = re.sub(
                r'\{\{#each contents\}\}.*?\{\{/each\}\}',
                contents_html,
                html_output,
                flags=re.DOTALL
            )
            html_output = re.sub(
                r'\{\{#each timetable\}\}.*?\{\{/each\}\}',
                timetable_html,
                html_output,
                flags=re.DOTALL
            )
            html_output = re.sub(
                r'\{\{#each targets\}\}.*?\{\{/each\}\}',
                targets_html,
                html_output,
                flags=re.DOTALL
            )

            # 生成完了
            st.success("✅ LPを生成しました！")

            # プレビュー
            st.subheader("プレビュー")
            st.components.v1.html(html_output, height=800, scrolling=True)

            # ダウンロード
            st.divider()
            st.subheader("📥 ダウンロード")

            st.download_button(
                label="HTMLファイルをダウンロード",
                data=html_output,
                file_name="index.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )

            # GitHub Pages公開手順
            st.divider()
            st.subheader("🌐 GitHub Pagesで公開する方法")

            st.markdown("""
            1. **GitHubにログイン** → https://github.com

            2. **新しいリポジトリを作成**
               - 右上の「+」→「New repository」
               - Repository name: `webinar-lp-20250930`（任意）
               - 「Public」を選択
               - 「Create repository」をクリック

            3. **ファイルをアップロード**
               - 「uploading an existing file」をクリック
               - ダウンロードした `index.html` をドラッグ＆ドロップ
               - 「Commit changes」をクリック

            4. **GitHub Pagesを有効化**
               - リポジトリの「Settings」タブ
               - 左メニュー「Pages」
               - Source: 「Deploy from a branch」
               - Branch: 「main」→「/(root)」→「Save」

            5. **公開完了！**
               - 数分待つと `https://あなたのユーザー名.github.io/webinar-lp-20250930/` で公開されます
            """)
