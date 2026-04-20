---
title: "Notes"
permalink: /notes/
layout: archive
---

Short reference material — things I want to remember or come back to.

{% for post in site.categories.notes %}
  {% include archive-single.html %}
{% endfor %}
