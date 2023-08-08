###選択肢でじゃんけん 完成　Streamlitにあげる

#必要なライブラリをインポート
import streamlit as st
from PIL import Image
import time
import random
import pandas as pd
from xgboost import XGBClassifier

# データセットの読み込み
# GitHubリポジトリ内のファイル相対パス
file_relative_path = 'DataFrame.csv'

# データを読み込む
@st.cache
def load_data():
    data = pd.read_csv(file_relative_path)
    return df

# データを読み込む
df = load_data()


# 目標値（目的変数）の指定
target_column = 'target'  # 目標値の列名を適宜変更する必要があります
y = df[target_column]
x = df.drop(target_column, axis=1)  # 目標値を除いた特徴量をXとして使用

# 予測モデルの構築
model = XGBClassifier(booster="gbtree",             # ブースター種類（ツリーモデル：gbtree or dart, 線形モデル：gblinear)
                        learning_rate=1,              # 過学習防止を目的とした学習率
                        min_split_loss=0,             # 決定木の葉ノード追加に伴う損失減少の下限値
                        max_depth=6,                  # 決定木の深さの最大値
                        min_child_weight=1,           # 決定木の葉に必要な重みの下限
                        subsample=1,                  # 各決定木においてランダム抽出されるサンプル割合
                        sampling_method="uniform",    # サンプリング方法
                        colsample_bytree=1,           # 各決定木でランダムに設定される説明変数の割合
                        colsample_bylevel=1,          # 決定木が深さ単位で分割される際に利用する説明変数の割合
                        reg_lambda=1,                 # L2正則化のペナルティ項
                        reg_alpha=0,                  # L1正則化のペナルティ項
                        tree_method="auto",           # ツリー構造アルゴリズム
                        process_type="default",       # 実行するブースティングプロセス
                        grow_policy="depthwise",      # 新しい葉ノードを木に追加する際の制御ポリシー
                        max_leaves=0,                 # 追加する葉ノードの最大数
                        objective="reg:squarederror", # 学習プロセスで最小化を目指す損失関数
                        num_round=9,                  # ブースティング回数(=作成する決定木の本数)
                        )
model.fit(x, y)

# ダメだったモデル RandomForestRegressor / GradientBoostingRegressor


#　タイトルとテキストを記入
st.title('AI じゃん・けん・ぽん')

# それぞれの手の画像を読み込む
# COM と ユーザー それぞれ45度かたむける
image0 = Image.open('ぐー.png')
im_rotate0_com = image0.rotate(45, expand=True) #COM用
im_rotate0_user = image0.rotate(-45, expand=True) #ユーザー用
image1 = Image.open('ちょき.png')
im_rotate1_com = image1.rotate(45, expand=True) #COM用
im_rotate1_user = image1.rotate(-45, expand=True) #ユーザー用
image2 = Image.open('ぱー.png')
im_rotate2_com = image2.rotate(45, expand=True) #COM用
im_rotate2_user = image2.rotate(-45, expand=True) #ユーザー用

# 変数に代入する
choices = ['ぐー　', 'ちょき', 'ぱー　']
choices_mapping = {0: 'ぐー', 1: 'ちょき', 2: 'ぱー', 3:'-'}
# 対戦結果のグーチョキパーそれぞれの加算数値を 0 に初期化する
result0 = 0
result1 = 0
result2 = 0
hand = 0
win_lose = 0
if "n" not in st.session_state:
    st.session_state.n = 3
if "X1" not in st.session_state:
    st.session_state.X1 = 3
if "X2" not in st.session_state:
    st.session_state.X2 = 3
if "X3" not in st.session_state:
    st.session_state.X3 = 3


# 以下サイドバーの内容
# どの手を出すか選択するボタンを表示
with st.sidebar:

    st.header('出す手を選んでください')
    btn1, btn2,btn3 = st.columns(3)
    with btn1:
        clicked1 = st.button(choices[0]) # ぐーボタン
    with btn2:
        clicked2 = st.button(choices[1]) # ちょきボタン
    with btn3:
        clicked3 = st.button(choices[2]) # ぱーボタン

    st.header('対戦回数')
    # ボタンのクリック回数をカウントする変数
    # session_state は過去の数値を引き継いで加算する
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0
        st.write(f'{st.session_state.click_count} 回')

    # ３つのボタンどれかをクリックすると回数を加算する
    if clicked1 or clicked2 or clicked3:
        st.session_state.click_count += 1
        # ボタンのクリック回数の表示
        st.write(f'{st.session_state.click_count} 回')


    st.header('対戦成績')
    # 対戦成績の回数をセット
    win_col, lose_col, eql_col = st.columns(3)
    if "win" not in st.session_state:
        st.session_state.win = 0
    if "lose" not in st.session_state:
        st.session_state.lose = 0
    if "eql" not in st.session_state:
        st.session_state.eql = 0

    # データフレームで対戦ログを表示
    st.write('※ぐー: 0　ちょき: 1　ぱー: 2')
    if "hand_log" not in st.session_state:
        df_new = pd.DataFrame(columns=['あなた', 'COM', '結果'])
        st.session_state.hand_log = df_new
        st.write(df_new)

# COMが出す手をランダムで決める
if st.session_state.click_count < 4:
    st.session_state.n = random.randint(0, 2)
    print('random')
    print(st.session_state.n)
#else:
    # 学習用のデータとして手の履歴を取得
    #df_new = st.session_state.hand_log
    #print(df_new)
    #if len(df_new) > 0:
        #X_Value = pd.DataFrame([[st.session_state.X3, st.session_state.X2, st.session_state.X1]])
        # 予測値のデータフレーム
        #n = model.predict_proba(X_Value)
        #print(X_Value)
        #print(n)
        # 最大要素のインデックスを取得
        #n = np.argmax(n)
        #print(n)
        #print('model')


# 手のボタン をクリックすると、イベント開始
if clicked1 or clicked2 or clicked3:
    # じゃん・けん・ぽん を順番に表示
    jyan_col1, ken_col2, pon_col3 = st.columns(3)
    with jyan_col1:
        time.sleep(0.5)
        st.subheader('じゃん')
    with ken_col2:
        time.sleep(0.5)
        st.subheader('けん')
    with pon_col3:
        time.sleep(0.5)
        st.subheader('ぽん')

    # coa2(選んだユーザーの手)、col3(ランダムのCOMの手)を表示させる配置を設定'
    boy_col1, user_col2, com_col3, robot_col4 = st.columns(4)

    # ユーザーの手の画像を表示
    st.session_state.X3 = st.session_state.X2
    st.session_state.X2 = st.session_state.X1
    
    with boy_col1:
        boy = Image.open('男の子.png')
        st.image(boy, width=200)

    with user_col2:
        if clicked1:
            st.image(im_rotate0_user, width=220)
            hand = 0
            st.session_state.X1 = 0
        elif clicked2:
            st.image(im_rotate1_user, width=200)
            hand = 1
            st.session_state.X1 = 1
        else:
            st.image(im_rotate2_user, width=200)
            hand = 2
            st.session_state.X1 = 2

    # COMの手の画像を表示
    with com_col3:
        if st.session_state.n == 0:
            st.image(im_rotate0_com, width=220)
        elif st.session_state.n == 1:
            st.image(im_rotate1_com, width=200)
        else:
            st.image(im_rotate2_com, width=200)

    with robot_col4:
        robot = Image.open('ロボット.png')
        st.image(robot, width=200)


    if hand == 0 and st.session_state.n == 0: #ぐーvsぐー
        st.header('あいこ')
        result2 = 1
    elif hand == 0 and st.session_state.n == 1: #ぐーvsちょき
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 0 and st.session_state.n == 2: #ぐーvsぱー
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 1 and st.session_state.n == 0: #ちょきvsぐー
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 1 and st.session_state.n == 1: #ちょきvsちょき
        st.header('あいこ')
        result2 = 1
    elif hand == 1 and st.session_state.n == 2: #ちょきvsぱー
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 2 and st.session_state.n == 0: #ぱーvsぐー
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 2 and st.session_state.n == 1: #ぱーvsちょき
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 2 and st.session_state.n == 2: #ぱーvsぱー
        st.header('あいこ')
        result2 = 1

    st.session_state.win += result0
    st.session_state.lose += result1
    st.session_state.eql += result2

    if result0 == 1:
        win_lose = "〇"
    elif result1 == 1:
        win_lose = "×"
    elif result2 == 1:
        win_lose = "△"

    #st.write('2回前:', choices_mapping[st.session_state['X2']])
    df_new = pd.DataFrame({'あなた': choices_mapping[hand], 'COM': choices_mapping[st.session_state.n], '結果': [win_lose]})
    st.session_state.hand_log = pd.concat([st.session_state.hand_log, df_new], axis=0).reset_index(drop=True)
    st.sidebar.dataframe(st.session_state.hand_log)


    log_col1, pred_col2 = st.columns(2)
    with log_col1:
        st.write('1回前:', choices_mapping[st.session_state['X1']])
        st.write('2回前:', choices_mapping[st.session_state['X2']])
        st.write('3回前:', choices_mapping[st.session_state['X3']])

    with pred_col2:
        # データフレームを作成
        X_Value = pd.DataFrame([[st.session_state.X3, st.session_state.X2, st.session_state.X1]], columns=['X3', 'X2', 'X1'])
        # 予測値のデータフレーム
#        st.session_state.n = model.predict_proba(X_Value)
        st.session_state.n = model.predict(X_Value)
        print(X_Value)
        print(st.session_state.n)
        st.session_state.n = st.session_state.n.item()
        print(st.session_state.n)
        if st.session_state.click_count > 2:
            st.write('robot が次に出そうとしている手:', choices_mapping[st.session_state['n']])



with win_col:
    st.write(f'勝ち {st.session_state.win} 回')
with lose_col:
    st.write(f'負け {st.session_state.lose} 回')
with eql_col:
    st.write(f'あいこ {st.session_state.eql} 回')

