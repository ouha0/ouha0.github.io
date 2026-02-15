---
title: "My Library"
permalink: /library/
layout: single
author_profile: true
---

Some useful resources

## Math

{% for book in site.data.library %}
{% if book.category == "Math" %}

* **[{{ book.title }}]({{ book.link }})** by {{ book.author }} <br>_{{ book.description }}_
{% endif %}
{% endfor %}

## Computer Science

{% for book in site.data.library %}
{% if book.category == "Computer Science" %}

* **[{{ book.title }}]({{ book.link }})** by {{ book.author }} <br>_{{ book.description }}_
{% endif %}
{% endfor %}
