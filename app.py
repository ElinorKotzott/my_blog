import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        with open("data.json", "r") as handle:
            blog_posts = json.load(handle)

        new_post = {
            "id": len(blog_posts) + 1,
            "title": title,
            "author": author,
            "content": content
        }

        blog_posts.append(new_post)

        with open("data.json", "w") as handle:
            json.dump(blog_posts, handle)

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


