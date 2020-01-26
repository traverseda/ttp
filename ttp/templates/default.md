# {{project}}
## {{start.format('dddd, MMMM Do, YYYY')}} to {{end.format('dddd, MMMM Do, YYYY')}}
{%- if week %}
### Week {{week}}
{%- endif %}
{% for task in tasks %}
 * {{"{:5.2f}".format(task.span.seconds/3600)}}h {{ task.msg }}
{%- endfor %}

{{round(total/3600,2)}} hours worked total
