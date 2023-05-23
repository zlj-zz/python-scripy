import re

html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title></title>
    <style type="text/css">
        body {{
            background: url(images/bg.jpg);
            background-size: cover;
            /*overflow: hidden;*/
        }}

        #piclist {{
            /* width: 750px; */
            height: 560px;
            margin: 35px auto;

        }}

        #piclist img {{
            /* width: 230px; */
            height: 260px;
            padding: 5px;
            border: 5px solid black;
            float: left;
            display: block;
            /*设置为3D元素*/
            transform-style: preserve-3d;
            /*过度*/
            transition: 2s;
            /*阴影*/
            box-shadow: 0px 0px 20px black;
        }}

        #piclist img:hover {{
            /*transform: rotateY(360deg);*/
        }}

        #mask {{
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            position: absolute;
            background: #000000;
            /*透明度*/
            opacity: 0.5;
            /*隐藏*/
            display: none;
        }}
    </style>
</head>

<body>
    <div id="piclist">
        <div id="app"></div>
    </div>
    <div id="mask"></div>

</body>

<script type="text/javascript">
    let app = document.getElementById('app')

    let list = [{url_list}];

    for (url of list){{
        let img = document.createElement('img')
        img.src = url
        app.appendChild(img)
    }}

</script>

</html>
"""

if __name__ == "__main__":
    path = "./urls.txt"
    output = "./test.html"
    
    content = open(path).read()

    re_str = r"Url: (.*?)\n"
    items = re.compile(re_str).findall(content)

    with open(output, "w") as fp:

        # print(html_template.format(url_list=",".join(f"{url}" for url in items)))
        fp.write(html_template.format(url_list=",".join(f"'{url}'" for url in items)))
