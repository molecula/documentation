#!/opt/homebrew/bin/python3

from bs4 import BeautifulSoup

with open('extract.css', 'r') as f:
    css = f.read()


with open('sql3.html', 'r') as f:

    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    for sect in soup.find_all('section'):
        print(sect.h4)

        svg = sect.svg
        svg["xmlns"] = "http://www.w3.org/2000/svg"
        del svg["style"]
        viewbox = svg["viewbox"]
        items = viewbox.split(' ')

        svg['height'] = items[3]

        new_style = soup.new_tag("style")
        new_style.string = css
        svg.append(new_style)

        # get rid of a's
        for a in svg.find_all('a'):
            del a["xlink:href"]

        filename = "./../" + sect.h4.string + '.svg'

        text_file = open(filename, "w")

        svgbody = svg.prettify()
        n = text_file.write(svgbody)
        text_file.close()
