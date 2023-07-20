#必要なライブラリをインポート
import streamlit as st
import numpy as np
from PIL import Image
import time
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier

#　タイトルとテキストを記入
st.title('AI じゃん・けん・ぽん')

# トップ画像を読み込み、表示する
# image3 = Image.open('ぐーちょきぱー.png')
# st.image(image3)



# それぞれの手の画像を読み込む
image0 = Image.open('ぐー.png')
image1 = Image.open('ちょき.png')
image2 = Image.open('ぱー.png')
choices = ['ぐー', 'ちょき', 'ぱー']
choices_mapping = {'ぐー': 0, 'ちょき': 1, 'ぱー': 2}
result0 = 0
result1 = 0
result2 = 0


# 以下サイドバーの内容
# どの手を出すか選択するラジオボタンを表示
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
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0
        st.write(f'{st.session_state.click_count} 回')
    
    if clicked1 or clicked2 or clicked3:
        st.session_state.click_count += 1
        # ボタンのクリック回数の表示
        st.write(f'{st.session_state.click_count} 回')


    st.header('対戦成績')
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
        st.session_state.hand_log = pd.DataFrame(columns=['あなた', 'COM', '結果'])
    
#    col0, col1, col2 = st.columns(3)
        df_new = pd.DataFrame(columns=['あなた', 'COM', '結果'])
        #st.write(df_new)

# COMが出す手をランダムで決める
if st.session_state.click_count < 6:
    n = random.randint(0, 2)
    print('random')
else:
    # 学習用のデータとして手の履歴を取得
    df_new = st.session_state.hand_log
    #print(df_new)
    if len(df_new) > 0:
        x = df_new['あなた'].values[:-1]
        x = x.reshape(-1, 1)
        t = df_new['COM'].values[1:]
        t = t.astype(int)
        model = DecisionTreeClassifier()
        # model = RandomForestClassifier() #決定木でもいい
        #model = XGBClassifier()
        model.fit(x, t)
        n = model.predict([[df_new.iloc[-1]['あなた']]])
        if n == 0:
            n = 2
        elif n == 1:
            n = 0
        else:
            n = 1
        print('gx')

# 手のボタン をクリックすると、イベント開始
if clicked1 or clicked2 or clicked3:

    # じゃん・けん・ぽん を順番に表示
    col1, col2, col3 = st.columns(3)
    with col1:
        time.sleep(0.5)
        st.subheader('じゃん')
    with col2:
        time.sleep(0.5)
        st.subheader('けん')
    with col3:
        time.sleep(0.5)
        st.subheader('ぽん')

    # coa1(選んだユーザーの手)、col2(ランダムのCOMの手)を表示させる配置を設定'
    col1, col2 = st.columns(2)

    # ユーザーの手の画像を表示
    with col1:
        if clicked1:
            st.image(image0, width=250)
            hand = 0
        elif clicked2:
            st.image(image1, width=200)
            hand = 1
        else:
            st.image(image2, width=240)
            hand = 2

    # COMの手の画像を表示
    with col2:
        if n == 0:
            st.image(image0, width=250)
        elif n == 1:
            st.image(image1, width=200)
        else:
            st.image(image2, width=240)

    if hand == 0 and n == 0: #ぐーvsぐー
        st.header('あいこ')
        result2 = 1
    elif hand == 0 and n == 1: #ぐーvsちょき
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 0 and n == 2: #ぐーvsぱー
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 1 and n == 0: #ちょきvsぐー
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 1 and n == 1: #ちょきvsちょき
        st.header('あいこ')
        result2 = 1
    elif hand == 1 and n == 2: #ちょきvsぱー
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 2 and n == 0: #ぱーvsぐー
        st.header('あなたの 勝ち')
        result0 = 1
    elif hand == 2 and n == 1: #ぱーvsちょき
        st.header('あなたの 負け')
        result1 = 1
    elif hand == 2 and n == 2: #ぱーvsぱー
        st.header('あいこ')
        result2 = 1

    st.session_state.win += result0
    st.session_state.lose += result1
    st.session_state.eql += result2

    with win_col:
        st.write(f'勝ち {st.session_state.win} 回')
    with lose_col:
        st.write(f'負け {st.session_state.lose} 回')
    with eql_col:
        st.write(f'あいこ {st.session_state.eql} 回')

    # COMが勝つ手を計算
    #if hand == 0:
    #    win_hand = 2
    #elif hand == 1:
    #    win_hand = 0
    #else:
    #    win_hand = 1
    if result0 == 1:
        win_lose = "〇"
    elif result1 == 1:
        win_lose = "×"
    else:
        win_lose = "△"

    df_new = pd.DataFrame({'あなた': [hand], 'COM': [n], '結果': [win_lose]})
    st.session_state.hand_log = pd.concat([st.session_state.hand_log, df_new], axis=0).reset_index(drop=True)
    st.sidebar.dataframe(st.session_state.hand_log)
