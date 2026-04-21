---
title: "Notes"
permalink: /notes/
layout: archive
---

Short reference material.

{% for post in site.categories.notes %}
  {% include archive-single.html %}
{% endfor %}
