import json
from flask import Flask, request, render_template, redirect, url_for

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

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open("data.json", "w") as handle:
        json.dump(blog_posts, handle)

    return redirect(url_for('index'))



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)

    blog_post = next((post for post in blog_posts if post["id"] == post_id), None)

    if blog_post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        if title:
            blog_post["title"] = title
        if author:
            blog_post["author"] = author
        if content:
            blog_post["content"] = content

        with open("data.json", "w") as handle:
            json.dump(blog_posts, handle)

        return redirect(url_for('index'))

    return render_template('update.html', post=blog_post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


