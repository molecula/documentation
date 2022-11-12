---
layout: blank
---
documents = [
{% capture firstN %}{{ site.posts.size | minus: 1 }}{% endcapture %}
{% for post in site.posts limit: firstN %}
  {% capture body %}{{ post.content | strip_html | replace: '
', ' ' | replace: '"', "" | replace: "\", "" }}{% endcapture %}
  {
    title : "{{ post.title }}",
    body  : "{{ body }}",
    url   : "{{ post.url }}"{% if post.tags != empty %},
    tags  : "{{ post.tags | sort | join: ','}}"
    {% endif %}
  },
{% endfor %}
{% capture post %}{{ site.posts | last }}{% endcapture %}
{% capture body %}{{ post.content | strip_html | replace '
', ' ' | replace: '"', "" | replace: "\", ""  }}{% endcapture %}
  {
    title : "{{ post.title }}",
    body  : "{{ body }}",
    url   : "{{ post.url }}"{% if post.tags.size %},
    tags  : "{{ post.tags | sort | join: ','}}"
    {% endif %}
  }
];