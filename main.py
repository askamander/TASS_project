import gower
import numpy as np
import pandas as pd
from flask import Flask
from flask import request, escape



app = Flask(__name__)
df = pd.read_csv('data/pg_authors_clean.csv')
df_orig = pd.read_csv('data/pg_authors.csv')


@app.route("/")
def index():

    book = str(escape(request.args.get("book", "")))
    num = int(escape(request.args.get("num", "10")))
    if book:

        table = load_books(book, num)

    else:

        table = ""

    return (

        """
        <form action="" method="get">
                search: <input type="text" name="book">
                <input type="submit" value="See similar books">
            </form>"""
        + f"Recommendations for {book}: "

        + table

    )


def load_books(book_title, num):
    books_to_recommend_num = num
    global df, df_orig

    if df_orig.loc[df_orig['Title'] == book_title].empty:
        return '<br>Book not in Project Gutenberg resources'

    idx = df_orig.loc[df_orig['Title'] == book_title].index[0]
    topn = gower.gower_topn(df.iloc[idx:idx + 1, :], df, n=books_to_recommend_num)
    recommendations = {'books': df_orig.iloc[topn['index'][1:]]["Title"].tolist(),
                                                 'authors': df_orig.iloc[topn['index'][1:]]["Authors"].tolist(),
                                                 'issued': df_orig.iloc[topn['index'][1:]]["Issued"].tolist(),
                                                 'similarities': topn['values'].tolist(),
                                                 'index': df_orig.iloc[topn['index'][1:]]["Text#"].tolist()}
    try:
        table = """<table><tr>
            <th>Title</th>
            <th>Authors</th>
            <th>Issued</th>
            <th>Dissimilarity</th>
            <th>Link</th>
          </tr>"""
        for j in range(int(books_to_recommend_num-1)):
            table = table + f"""<tr>
                <td>{recommendations['books'][j]}</td>
                <td>{recommendations['authors'][j]}</td>
                <td>{recommendations['issued'][j]}</td>
                <td>{recommendations['similarities'][j]:.5f}</td>
                <td>
                    <a href="https://www.gutenberg.org/ebooks/{recommendations['index'][j]}">link</a>
                </td>
              </tr>"""
        return str(table)

    except ValueError:

        return "invalid input"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)