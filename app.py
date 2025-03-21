import json
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    """displays blog posts on home"""
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """allows user to add a new post, saves input into variables, creates new
    post, adds it to the dictionary and overwrites json data"""
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
    """allows user to delete a post. reads blog posts and loops through them,
    saving all except the one to delete, then overwriting the json data"""
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open("data.json", "w") as handle:
        json.dump(blog_posts, handle)

    return redirect(url_for('index'))



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """allows user to update dictionary. loads data for the chosen blog post, displays form and
    saves changes to data. redirects to home"""
    with open("data.json", "r") as handle:
        blog_posts = json.load(handle)

    #finding blog post with the correct id
    blog_post = next((post for post in blog_posts if post["id"] == post_id), None)

    if blog_post is None:
        return "Post not found", 404

    #assigning form input to variables
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        #updating dictionary
        if title:
            blog_post["title"] = title
        if author:
            blog_post["author"] = author
        if content:
            blog_post["content"] = content

        #overwriting data with updated data
        with open("data.json", "w") as handle:
            json.dump(blog_posts, handle)

        return redirect(url_for('index'))

    return render_template('update.html', post=blog_post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


