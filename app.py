from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

top_books = pickle.load(open("top_books.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
books_users_matrix = pickle.load(open("books_users_matrix.pkl","rb"))
data = pickle.load(open('data.pkl',"rb"))

# def recommend_book(book_title):
#     index_of_book = np.where(books_users_matrix.index == book_title)[0][0]
#     recommended_books = np.argsort(similarity[index_of_book])[-8:-1][::-1]
#     books = []
#     for i in recommended_books:
#         books.append(books_users_matrix.index[i])
#     return books

# print(top_books)
app = Flask(__name__)
@app.route('/')

def index():
    return render_template('index.html',
                           book_name=list(top_books['Book-Title'].values),
                           author=list(top_books['Book-Author'].values),
                           image=list(top_books['Image-URL-L'].values),
                           votes=list(top_books['count'].values),
                           ratings=list(top_books['mean'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    # return "hello"
    user_input = request.form.get('User-Input')
    index_of_book = np.where(books_users_matrix.index == user_input)[0][0]
    recommended_books = np.argsort(similarity[index_of_book])[-8:-1][::-1]
    data2 = []
    for i in recommended_books:
        l = []
        l.append(books_users_matrix.index[i])
        l.append(data[data['Book-Title'] == books_users_matrix.index[i]].iloc[0][
                     'Book-Author'])
        l.append(data[data['Book-Title'] == books_users_matrix.index[i]].iloc[0][
                     'Image-URL-L'])
        data2.append(l)
    print(data2)
    return render_template('recommend.html',data=data2)

if __name__ == '__main__':
    app.run(debug=True)